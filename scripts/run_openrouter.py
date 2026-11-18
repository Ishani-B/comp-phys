"""Send every item to a model on OpenRouter and write one row per call.

Run from the repo root. The key is read from the OPENROUTER_API_KEY environment
variable, or from a .env file in the repo root (ignored by git). Never commit it.

    python3 scripts/run_openrouter.py --conditions real
    python3 scripts/run_openrouter.py --conditions near far --append
    python3 scripts/run_openrouter.py --dry-run      # show the first request, send nothing

Defaults: google/gemma-4-31b-it, pinned to one provider (Crusoe, bf16) with no
fallback to other providers, temperature 0, seed 0, at most 4096 output tokens,
reasoning (thinking) off. Each call is a new chat with one user message.

The run log has the same core columns as scripts/run_ollama.py, so
scripts/score.py scores it unchanged. Only the Python standard library is used.
"""

import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://openrouter.ai/api/v1/chat/completions"

COLUMNS = [
    "run_id", "call_index", "timestamp_utc", "item_id", "law_distance", "law_variant",
    "test_t", "prompt_id", "model", "model_served", "provider", "quantization", "generation_id",
    "temperature", "seed", "max_tokens", "reasoning_setting", "response", "reasoning_text",
    "done_reason", "prompt_tokens", "output_tokens", "reasoning_tokens", "cost_usd",
    "duration_s", "cf_answer", "real_answer",
]


def load_key():
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    env_path = os.path.join(ROOT, ".env")
    if not key and os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                name, _, value = line.strip().partition("=")
                if name.strip() == "OPENROUTER_API_KEY":
                    key = value.strip().strip("'\"")
    if not key:
        raise SystemExit("No OPENROUTER_API_KEY found in the environment or in .env")
    return key


def call(payload, key, tries=10):
    """POST with retries on rate limits and server errors (waits 15s, 30s, ... up to 120s).
    Raises after the last try."""
    body = json.dumps(payload).encode()
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(URL, data=body, headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Title": "counterfactual-physics-starter",
        })
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.load(r)
            if "error" in data:
                raise RuntimeError(f"OpenRouter error: {data['error']}")
            return data
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and attempt < tries:
                wait = min(15 * attempt, 120)
                print(f"    HTTP {e.code}, retrying in {wait}s: {detail[:120]}")
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < tries:
                print(f"    network error, retrying: {e}")
                time.sleep(10 * attempt)
                continue
            raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="google/gemma-4-31b-it")
    ap.add_argument("--provider", default="crusoe", help="OpenRouter provider slug to pin to")
    ap.add_argument("--quantization", default="bf16")
    ap.add_argument("--data", default=os.path.join(ROOT, "data", "freefall_starter.csv"))
    ap.add_argument("--out", default=None, help="CSV run log (default: results/run_log_<model>.csv)")
    ap.add_argument("--conditions", nargs="+", default=["real", "near", "far"])
    ap.add_argument("--append", action="store_true")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--reasoning", choices=["off", "on"], default="off")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    slug = args.model.split("/")[-1]
    out = args.out or os.path.join(ROOT, "results", f"run_log_{slug}.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(args.data, newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    queue = [it for cond in args.conditions for it in items if it["law_distance"] == cond]

    def payload(it):
        return {
            "model": args.model,
            "messages": [{"role": "user", "content": it["prompt"]}],  # new context every call
            "temperature": args.temperature,
            "seed": args.seed,
            "max_tokens": args.max_tokens,
            "reasoning": {"enabled": args.reasoning == "on"},
            "provider": {
                "order": [args.provider],
                "allow_fallbacks": False,          # every call goes to the same provider
                "quantizations": [args.quantization],
                "require_parameters": True,        # fail rather than silently drop seed/temperature
            },
            "usage": {"include": True},
        }

    if args.dry_run:
        print(json.dumps(payload(queue[0]), indent=2))
        print(f"\n{len(queue)} calls would be sent to {args.model} via {args.provider}; nothing sent.")
        return

    key = load_key()
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    existing = 0
    if args.append and os.path.exists(out):
        with open(out, newline="", encoding="utf-8") as f:
            done = [r["item_id"] for r in csv.DictReader(f)]
        existing = len(done)
        skipped = [it["item_id"] for it in queue if it["item_id"] in done]
        queue = [it for it in queue if it["item_id"] not in done]  # resume: never call an item twice
        if skipped:
            print(f"skipping {len(skipped)} item(s) already in the log: {', '.join(skipped)}")
    mode = "a" if args.append and os.path.exists(out) else "w"
    print(f"run {run_id}: {len(queue)} calls to {args.model} via {args.provider} ({args.quantization}), "
          f"temperature {args.temperature}, reasoning {args.reasoning}")

    total_cost = 0.0
    with open(out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if mode == "w":
            writer.writeheader()
        for i, it in enumerate(queue, start=existing + 1):
            t0 = time.time()
            data = call(payload(it), key)
            choice = data["choices"][0]
            msg = choice.get("message", {})
            usage = data.get("usage", {}) or {}
            details = usage.get("completion_tokens_details") or {}
            cost = usage.get("cost", "")
            if isinstance(cost, (int, float)):
                total_cost += cost
            writer.writerow({
                "run_id": run_id,
                "call_index": i,
                "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "item_id": it["item_id"],
                "law_distance": it["law_distance"],
                "law_variant": it["law_variant"],
                "test_t": it["test_t"],
                "prompt_id": it["prompt_id"],
                "model": args.model,
                "model_served": data.get("model", ""),
                "provider": data.get("provider", ""),
                "quantization": args.quantization,
                "generation_id": data.get("id", ""),
                "temperature": args.temperature,
                "seed": args.seed,
                "max_tokens": args.max_tokens,
                "reasoning_setting": args.reasoning,
                "response": msg.get("content") or "",
                "reasoning_text": msg.get("reasoning") or "",
                "done_reason": choice.get("finish_reason", ""),
                "prompt_tokens": usage.get("prompt_tokens", ""),
                "output_tokens": usage.get("completion_tokens", ""),
                "reasoning_tokens": details.get("reasoning_tokens", ""),
                "cost_usd": cost,
                "duration_s": round(time.time() - t0, 2),
                "cf_answer": it["cf_answer"],
                "real_answer": it["real_answer"],
            })
            f.flush()
            print(f"  [{i}] {it['item_id']} done ({usage.get('completion_tokens', '?')} tokens, "
                  f"{choice.get('finish_reason', '')}, {data.get('provider', '?')})")
            time.sleep(3)  # be gentle with the provider's shared rate limit
    print(f"Wrote {len(queue)} rows to {os.path.relpath(out, ROOT)}; cost ${total_cost:.4f}")


if __name__ == "__main__":
    main()
