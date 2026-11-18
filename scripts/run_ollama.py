"""Send every item to a local model through Ollama and write one row per call.

Run from the repo root, with `ollama serve` running:
    python3 scripts/run_ollama.py --model gemma3:1b --conditions real
    python3 scripts/run_ollama.py --model gemma3:1b --conditions near far --append

Each call is a new chat with one user message, so no call sees another call's
context. The model's full answer is saved, with the correct answer under both
the law in the data (cf_answer) and the real law (real_answer).

Only the Python standard library is used.
"""

import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLLAMA = "http://localhost:11434"

COLUMNS = [
    "run_id", "call_index", "timestamp_utc", "item_id", "law_distance", "law_variant",
    "test_t", "prompt_id", "model", "model_digest", "parameter_size", "quantization",
    "ollama_version", "temperature", "seed", "num_predict", "response", "done_reason",
    "prompt_tokens", "output_tokens", "duration_s", "cf_answer", "real_answer",
]


def post(path, payload, timeout=600):
    req = urllib.request.Request(
        OLLAMA + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def get(path):
    with urllib.request.urlopen(OLLAMA + path, timeout=30) as r:
        return json.load(r)


def model_info(model):
    """Exact version of the model: the digest Ollama stores it under, plus size and quantization."""
    show = post("/api/show", {"model": model})
    tags = get("/api/tags")["models"]
    digest = next((m["digest"] for m in tags if m["name"] == model or m["model"] == model), "")
    return {
        "model_digest": digest,
        "parameter_size": show["details"].get("parameter_size", ""),
        "quantization": show["details"].get("quantization_level", ""),
        "ollama_version": get("/api/version")["version"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Ollama model tag, e.g. gemma3:1b")
    ap.add_argument("--data", default=os.path.join(ROOT, "data", "freefall_starter.csv"))
    ap.add_argument("--out", default=None, help="CSV run log (default: results/run_log_<model>.csv)")
    ap.add_argument("--conditions", nargs="+", default=["real", "near", "far"],
                    help="law distances to run, in this order")
    ap.add_argument("--append", action="store_true", help="add rows to an existing run log")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--num-predict", type=int, default=1024, help="cap on output tokens per call")
    args = ap.parse_args()

    out = args.out or os.path.join(ROOT, "results", f"run_log_{args.model.replace(':', '-')}.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(args.data, newline="", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    queue = [it for cond in args.conditions for it in items if it["law_distance"] == cond]

    info = model_info(args.model)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    existing = 0
    if args.append and os.path.exists(out):
        with open(out, newline="", encoding="utf-8") as f:
            existing = sum(1 for _ in csv.DictReader(f))
    mode = "a" if args.append and os.path.exists(out) else "w"

    print(f"run {run_id}: {len(queue)} calls to {args.model} ({info['parameter_size']}, "
          f"{info['quantization']}, digest {info['model_digest'][:12]}), temperature {args.temperature}")

    with open(out, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if mode == "w":
            writer.writeheader()
        for i, it in enumerate(queue, start=existing + 1):
            t0 = time.time()
            resp = post("/api/chat", {
                "model": args.model,
                "messages": [{"role": "user", "content": it["prompt"]}],  # new context every call
                "stream": False,
                "options": {"temperature": args.temperature, "seed": args.seed,
                            "num_predict": args.num_predict},
            })
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
                **info,
                "temperature": args.temperature,
                "seed": args.seed,
                "num_predict": args.num_predict,
                "response": resp["message"]["content"],
                "done_reason": resp.get("done_reason", ""),
                "prompt_tokens": resp.get("prompt_eval_count", ""),
                "output_tokens": resp.get("eval_count", ""),
                "duration_s": round(time.time() - t0, 2),
                "cf_answer": it["cf_answer"],
                "real_answer": it["real_answer"],
            })
            f.flush()
            print(f"  [{i}] {it['item_id']} done ({resp.get('eval_count', '?')} tokens, "
                  f"{resp.get('done_reason', '')})")
    print(f"Wrote {len(queue)} rows to {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
