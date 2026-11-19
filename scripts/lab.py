"""Virtual lab: the model runs its own experiments with a measurement tool.

Design: "Virtual lab" in PLAN.md. Prompts P2 (physics framing) and P3 (neutral
framing) are in prompts/prompts.md.

Run from the repo root (key in .env as OPENROUTER_API_KEY):
    python3 scripts/lab.py --smoke                                  # 8 unscored mechanics-check episodes
    python3 scripts/lab.py --framing physics --readings exact       # one cell of 30 episodes
    python3 scripts/lab.py --framing physics --readings exact --append   # resume; never repeats an episode

Each cell writes results/run_log_lab_<framing>_<readings>.csv (one row per
episode, scored by scripts/score.py unchanged) and a raw JSONL of every API
request and response under results/lab_raw/.
"""

import argparse
import csv
import datetime as dt
import json
import os
import random
import re
import time

from generate_items import fmt
from generate_pilot import quad_fit, t2_fit
from run_openrouter import call, load_key

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "google/gemma-4-31b-it"
PROVIDER = "crusoe"
QUANT = "bf16"
SEED = 20261118
BUDGET = 8
T_MAX = 6.0
MAX_TURNS = 12
MAX_TOKENS = 4096
NOISE = 0.10

FRAMINGS = {
    "physics": {
        "prompt_id": "P2",
        "tool": "drop_ball",
        "arg": "seconds",
        "value": "meters",
        "prompt": (
            "You are in a lab on a planet. You can drop a ball and measure how far it has fallen, "
            "in meters, after any number of seconds you choose between 0 and 6, using the drop_ball "
            "tool. The drop tower only allows up to 6 seconds of fall, so you can't measure [T] "
            "seconds directly. You can take up to 8 measurements. Your goal is to work out how far "
            "the ball will have fallen after [T] seconds. When you're done measuring, state the rule "
            "you found, then end with 'Answer: X'."
        ),
        "tool_description": ("Drop the ball and measure how far it has fallen after the given number "
                             "of seconds. Returns the distance in meters."),
        "arg_description": "Time after release, in seconds. Must be greater than 0 and at most 6.",
        "left_key": "measurements_left",
        "out_of_range": "Only times between 0 and 6 seconds are possible.",
        "spent": "No measurements left. Give your answer.",
    },
    "neutral": {
        "prompt_id": "P3",
        "tool": "read_counter",
        "arg": "tocks",
        "value": "glims",
        "prompt": (
            "You are working with a device that has a dial and a counter. You can set the dial to any "
            "number of tocks you choose between 0 and 6 and read how many glims the counter shows, "
            "using the read_counter tool. The dial only goes up to 6 tocks, so you can't read [T] "
            "tocks directly. You can take up to 8 readings. Your goal is to work out how many glims "
            "the counter will show at [T] tocks. When you're done taking readings, state the rule "
            "you found, then end with 'Answer: X'."
        ),
        "tool_description": "Set the dial to the given number of tocks and read the counter. Returns the number of glims.",
        "arg_description": "Dial setting, in tocks. Must be greater than 0 and at most 6.",
        "left_key": "readings_left",
        "out_of_range": "Only dial settings between 0 and 6 tocks are possible.",
        "spent": "No readings left. Give your answer.",
    },
}

HOOKE_FRAMINGS = {
    "physics": {
        "prompt_id": "P6",
        "tool": "hang_weight",
        "arg": "grams",
        "value": "centimeters",
        "prompt": (
            "You are in a lab with a spring. You can hang any weight you choose between 0 and 600 grams "
            "on the spring and measure how far it stretches, in centimeters, using the hang_weight tool. "
            "The spring can only be tested with up to 600 grams, so you can't measure [T] grams directly. "
            "You can take up to 8 measurements. Your goal is to work out how far the spring will stretch "
            "with [T] grams. When you're done measuring, state the rule you found, then end with 'Answer: X'."
        ),
        "tool_description": "Hang the given weight on the spring and measure how far it stretches. Returns the stretch in centimeters.",
        "arg_description": "Weight to hang, in grams. Must be greater than 0 and at most 600.",
        "left_key": "measurements_left",
        "out_of_range": "Only weights between 0 and 600 grams are possible.",
        "spent": "No measurements left. Give your answer.",
    },
    "neutral": {
        "prompt_id": "P7",
        "tool": "read_counter",
        "arg": "tocks",
        "value": "glims",
        "prompt": (
            "You are working with a device that has a dial and a counter. You can set the dial to any "
            "number of tocks you choose between 0 and 600 and read how many glims the counter shows, "
            "using the read_counter tool. The dial only goes up to 600 tocks, so you can't read [T] "
            "tocks directly. You can take up to 8 readings. Your goal is to work out how many glims "
            "the counter will show at [T] tocks. When you're done taking readings, state the rule "
            "you found, then end with 'Answer: X'."
        ),
        "tool_description": "Set the dial to the given number of tocks and read the counter. Returns the number of glims.",
        "arg_description": "Dial setting, in tocks. Must be greater than 0 and at most 600.",
        "left_key": "readings_left",
        "out_of_range": "Only dial settings between 0 and 600 tocks are possible.",
        "spent": "No readings left. Give your answer.",
    },
}

# Each domain: its data, framings, measurement window, and the real law's form (for the familiar fit).
LAB_DOMAINS = {
    "freefall": {"data": "freefall_starter.csv", "framings": FRAMINGS, "scale": 1.0, "t_max": 6.0, "real_p": 2.0},
    "hooke": {"data": "hooke_standard.csv", "framings": HOOKE_FRAMINGS, "scale": 100.0, "t_max": 600.0, "real_p": 1.0},
}
# Model presets. Anthropic supports no seed and publishes no quantization.
LAB_MODELS = {
    "gemma": {"model": "google/gemma-4-31b-it", "provider": "crusoe", "quant": "bf16", "seed": True},
    "claude": {"model": "anthropic/claude-sonnet-4.6", "provider": "anthropic", "quant": None, "seed": False},
}

SMOKE_LAWS_HOOKE = [  # not among the 30 study laws; unscored
    {"item_id": "SMOKE-H1", "law_distance": "near", "law_variant": "smoke_p1.2", "formula": "y = 2.2 * (x/100)^1.2",
     "coefficient": "2.2", "exponent": "1.2", "test_t": "9", "test_x": "900"},
    {"item_id": "SMOKE-H2", "law_distance": "near", "law_variant": "smoke_p0.6", "formula": "y = 1.8 * (x/100)^0.6",
     "coefficient": "1.8", "exponent": "0.6", "test_t": "13", "test_x": "1300"},
]

SMOKE_LAWS = [  # not among the 30 study laws; unscored
    {"item_id": "SMOKE-1", "law_distance": "near", "law_variant": "smoke_t2", "formula": "d = 6 * t^2",
     "coefficient": "6", "exponent": "2", "test_t": "9"},
    {"item_id": "SMOKE-2", "law_distance": "far", "law_variant": "smoke_t3", "formula": "d = 0.8 * t^3",
     "coefficient": "0.8", "exponent": "3", "test_t": "12"},
]

COLUMNS = [
    "run_id", "call_index", "timestamp_utc", "item_id", "framing", "readings", "law_distance",
    "law_variant", "formula", "test_t", "prompt_id", "model", "model_served", "provider",
    "quantization", "temperature", "seed", "max_tokens", "reasoning_setting", "response",
    "transcript", "measurements", "n_measurements", "n_repeats", "n_invalid", "n_merged_calls", "n_turns",
    "done_reason", "physics_words", "prompt_tokens", "output_tokens", "reasoning_tokens",
    "cost_usd", "duration_s", "cf_answer", "real_answer", "t2_fit_answer", "quad_fit_answer",
    "domain", "test_x", "familiar_fit_answer",
]

# Run-time flag only. A bare "9.8" here also matched ordinary numbers like 19.8; compare_lab.py
# recomputes physics mentions with a stricter pattern, and that is the number reported.
PHYSICS_WORDS = re.compile(r"gravit|free.?fall|\\frac\{1\}\{2\}\s*g|accelerat|physics|earth|9\.8", re.I)


def call_with_deadline(payload, key, deadline=900, attempts=3):
    """call() with a hard overall deadline per request.

    urllib's timeout only bounds silence between chunks, so a stalled connection can hang
    for hours (seen in the supplementary rerun). Each attempt runs in a daemon thread; if it
    hasn't returned within `deadline` seconds it is abandoned and the request is retried.
    """
    import threading
    for attempt in range(1, attempts + 1):
        box = {}

        def work():
            try:
                box["data"] = call(payload, key, tries=20)
            except Exception as e:  # surfaced below
                box["error"] = e
        th = threading.Thread(target=work, daemon=True)
        th.start()
        th.join(deadline)
        if th.is_alive():
            print(f"    request hung for {deadline}s, retrying ({attempt}/{attempts})")
            continue
        if "error" in box:
            raise box["error"]
        return box["data"]
    raise TimeoutError(f"request hung {attempts} times")


def noise_factor(T, n):
    """Matched noise: the nth valid reading's factor depends only on the test time T and n."""
    return random.Random(f"{SEED}-{T}-{n}").uniform(1 - NOISE, 1 + NOISE)


class World:
    """One episode's lab: a hidden law, a budget, a window, and (optionally) matched noise."""

    def __init__(self, coefficient, exponent, T, framing, noisy, scale=1.0, t_max=T_MAX, framings=None):
        self.c, self.n, self.T = float(coefficient), float(exponent), int(T)
        self.f = (framings or FRAMINGS)[framing]
        self.noisy = noisy
        self.scale, self.t_max = float(scale), float(t_max)  # law is c * (t / scale) ** n, for 0 < t <= t_max
        self.readings = []   # (t, value) for every valid measurement, in order
        self.invalid = 0

    def measure(self, raw_args):
        """Handle one tool call. Returns the JSON-able result sent back to the model."""
        f = self.f
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args or {})
            value = args.get(f["arg"])
            if value is None:  # accept a misnamed argument if it is the only number given
                nums = [v for v in args.values() if isinstance(v, (int, float))]
                value = nums[0] if len(nums) == 1 else None
            t = round(float(value), 2)
        except (TypeError, ValueError, json.JSONDecodeError):
            self.invalid += 1
            return {"error": f"Could not read the {f['arg']} value. Give a number between 0 and {self.t_max:g}."}
        if len(self.readings) >= BUDGET:
            return {"error": f["spent"]}
        if not (0 < t <= self.t_max):
            self.invalid += 1
            return {"error": f["out_of_range"]}
        d = self.c * (t / self.scale) ** self.n
        if self.noisy:
            d *= noise_factor(self.T, len(self.readings) + 1)
        d = round(d, 3)
        self.readings.append((t, d))
        return {f["arg"]: t, f["value"]: d, f["left_key"]: BUDGET - len(self.readings)}


def split_tool_calls(tool_calls):
    """Normalize the model's tool calls so they can be echoed back and answered one by one.

    Gemma on Crusoe sometimes merges parallel calls into one call whose arguments are
    several JSON objects back to back, e.g. '{"seconds": 1}{"seconds": 2}'. Each object
    becomes its own call (ids suffixed _1, _2, ...). Arguments that aren't JSON at all are
    echoed as "{}" and keep their original text so the lab can reject them.
    Returns (calls, merged): calls are dicts with id, name, arguments (valid JSON), raw.
    """
    decoder = json.JSONDecoder()
    calls, merged = [], 0
    for tc in tool_calls:
        name = tc["function"]["name"]
        raw = tc["function"].get("arguments") or "{}"
        objs, pos, ok = [], 0, True
        while pos < len(raw):
            while pos < len(raw) and raw[pos] in " \n\t,":
                pos += 1
            if pos >= len(raw):
                break
            try:
                obj, pos = decoder.raw_decode(raw, pos)
                objs.append(obj)
            except json.JSONDecodeError:
                ok = False
                break
        if ok and len(objs) > 1:
            merged += 1
            for k, obj in enumerate(objs, start=1):
                calls.append({"id": f"{tc['id']}_{k}", "name": name, "arguments": json.dumps(obj), "raw": json.dumps(obj)})
        elif ok and len(objs) == 1:
            calls.append({"id": tc["id"], "name": name, "arguments": json.dumps(objs[0]), "raw": raw})
        else:
            calls.append({"id": tc["id"], "name": name, "arguments": "{}", "raw": raw})
    return calls, merged


def tool_spec(framing, framings=None):
    f = (framings or FRAMINGS)[framing]
    return [{"type": "function", "function": {
        "name": f["tool"], "description": f["tool_description"],
        "parameters": {"type": "object", "properties": {
            f["arg"]: {"type": "number", "description": f["arg_description"]}}, "required": [f["arg"]]}}}]


def render(messages):
    """Plain-text transcript of an episode."""
    out = []
    for m in messages:
        if m["role"] == "user":
            out.append(f"USER: {m['content']}")
        elif m["role"] == "assistant":
            if m.get("content"):
                out.append(f"MODEL: {m['content']}")
            for tc in m.get("tool_calls") or []:
                out.append(f"MODEL CALLS {tc['function']['name']}({tc['function']['arguments']})")
        elif m["role"] == "tool":
            out.append(f"TOOL: {m['content']}")
    return "\n\n".join(out)


def run_episode(item, framing, noisy, key, raw_file, max_tokens=MAX_TOKENS, domain="freefall", model="gemma"):
    D, M = LAB_DOMAINS[domain], LAB_MODELS[model]
    f = D["framings"][framing]
    T = int(item["test_t"])
    X = int(item.get("test_x") or T)  # the value asked about, in the prompt's units
    world = World(item["coefficient"], item["exponent"], T, framing, noisy,
                  scale=D["scale"], t_max=D["t_max"], framings=D["framings"])
    messages = [{"role": "user", "content": f["prompt"].replace("[T]", str(X))}]
    totals = {"prompt_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0, "cost_usd": 0.0}
    served, providers, final, done = set(), set(), "", "turn_cap"
    merged_total = 0
    t0 = time.time()
    turns = 0
    for turns in range(1, MAX_TURNS + 1):
        payload = {
            "model": M["model"], "messages": messages, "tools": tool_spec(framing, D["framings"]),
            "tool_choice": "auto", "temperature": 0.0, "max_tokens": max_tokens, "reasoning": {"enabled": False},
            "provider": {"order": [M["provider"]], "allow_fallbacks": False, "require_parameters": True},
            "usage": {"include": True},
        }
        if M["seed"]:
            payload["seed"] = 0
        if M["quant"]:
            payload["provider"]["quantizations"] = [M["quant"]]
        data = call_with_deadline(payload, key)  # patient with rate limits, and never hangs forever
        raw_file.write(json.dumps({"item_id": item["item_id"], "framing": framing, "noisy": noisy,
                                   "turn": turns, "request_messages": messages, "response": data}) + "\n")
        raw_file.flush()
        choice = data["choices"][0]
        msg = choice.get("message", {})
        usage = data.get("usage", {}) or {}
        totals["prompt_tokens"] += usage.get("prompt_tokens", 0) or 0
        totals["output_tokens"] += usage.get("completion_tokens", 0) or 0
        totals["reasoning_tokens"] += (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0
        totals["cost_usd"] += usage.get("cost", 0) or 0
        served.add(data.get("model", ""))
        providers.add(data.get("provider", ""))
        calls, merged = split_tool_calls(msg.get("tool_calls") or [])
        merged_total += merged
        assistant = {"role": "assistant", "content": msg.get("content") or ""}
        if calls:
            assistant["tool_calls"] = [{"id": c["id"], "type": "function",
                                        "function": {"name": c["name"], "arguments": c["arguments"]}}
                                       for c in calls]
        messages.append(assistant)
        if not calls:
            final, done = msg.get("content") or "", choice.get("finish_reason", "")
            break
        for c in calls:
            if c["name"] != f["tool"]:
                result = {"error": f"Unknown tool. Use {f['tool']}."}
            else:
                result = world.measure(c["raw"])
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(result)})
    ts = [t for t, _ in world.readings]
    ds = [d for _, d in world.readings]
    t2 = quad = familiar = ""
    if world.readings:
        if domain == "freefall":
            t2 = fmt(t2_fit(ts, ds, T))
        p = D["real_p"]  # the real law's form, constant fitted to the model's own readings
        k = sum(d * t ** p for t, d in world.readings) / sum(t ** (2 * p) for t in ts)
        familiar = fmt(k * X ** p)
    if len(set(ts)) >= 3:
        quad = fmt(quad_fit(ts, ds, X))
    model_text = " ".join(m.get("content", "") for m in messages if m["role"] == "assistant")
    return {
        "response": final,
        "transcript": render(messages),
        "measurements": json.dumps(world.readings),
        "n_measurements": len(world.readings),
        "n_repeats": len(ts) - len(set(ts)),
        "n_invalid": world.invalid,
        "n_merged_calls": merged_total,
        "n_turns": turns,
        "done_reason": done,
        "physics_words": "; ".join(sorted({m.group().lower() for m in PHYSICS_WORDS.finditer(model_text)})),
        "model_served": ", ".join(sorted(served)),
        "provider": ", ".join(sorted(providers)),
        **{k: (round(v, 8) if k == "cost_usd" else v) for k, v in totals.items()},
        "duration_s": round(time.time() - t0, 2),
        "t2_fit_answer": t2,
        "quad_fit_answer": quad,
        "familiar_fit_answer": familiar,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--framing", choices=list(FRAMINGS))
    ap.add_argument("--readings", choices=["exact", "noisy"])
    ap.add_argument("--conditions", nargs="+", default=["real", "near", "far"])
    ap.add_argument("--append", action="store_true", help="resume: skip episodes already in the log")
    ap.add_argument("--smoke", action="store_true", help="run the 8 unscored mechanics-check episodes")
    ap.add_argument("--max-tokens", type=int, default=MAX_TOKENS, help="per-turn output limit")
    ap.add_argument("--only", nargs="+", help="run only these item_ids (e.g. a pre-registered rerun)")
    ap.add_argument("--tag", default="", help="suffix for the log name, e.g. cap16k")
    ap.add_argument("--domain", choices=list(LAB_DOMAINS), default="freefall")
    ap.add_argument("--model", choices=list(LAB_MODELS), default="gemma")
    args = ap.parse_args()
    D, M = LAB_DOMAINS[args.domain], LAB_MODELS[args.model]
    original = args.domain == "freefall" and args.model == "gemma"  # keeps the first lab's file names

    def log_name(framing, readings):
        tag = "_" + args.tag if args.tag else ""
        return (f"run_log_lab_{framing}_{readings}{tag}" if original
                else f"run_log_lab_{args.domain}_{framing}_{readings}_{args.model}{tag}")

    if args.smoke:
        readings_list = ["exact", "noisy"] if args.domain == "freefall" else ["exact"]
        cells = [(fr, rd) for fr in D["framings"] for rd in readings_list]
        items = SMOKE_LAWS if args.domain == "freefall" else SMOKE_LAWS_HOOKE
        out_dir = os.path.join(ROOT, "results", "lab_smoke")
    else:
        if not (args.framing and args.readings):
            raise SystemExit("Give --framing and --readings, or --smoke")
        cells = [(args.framing, args.readings)]
        with open(os.path.join(ROOT, "data", D["data"]), newline="", encoding="utf-8") as f:
            all_items = list(csv.DictReader(f))
        items = [it for cond in args.conditions for it in all_items if it["law_distance"] == cond]
        if args.only:
            items = [it for it in items if it["item_id"] in set(args.only)]
        out_dir = os.path.join(ROOT, "results")
    os.makedirs(out_dir, exist_ok=True)
    raw_dir = os.path.join(out_dir if args.smoke else os.path.join(ROOT, "results"), "lab_raw")
    os.makedirs(raw_dir, exist_ok=True)
    key = load_key()

    for framing, readings in cells:
        noisy = readings == "noisy"
        out = os.path.join(out_dir, log_name(framing, readings) + ".csv")
        done_ids = []
        if args.append and os.path.exists(out):
            with open(out, newline="", encoding="utf-8") as f:
                done_ids = [r["item_id"] for r in csv.DictReader(f)]
        queue = [it for it in items if it["item_id"] not in done_ids]
        mode = "a" if args.append and os.path.exists(out) else "w"
        run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        print(f"run {run_id}: {len(queue)} episodes, {args.domain}, {framing} framing, {readings} readings, "
              f"{M['model']}" + (f" (skipping {len(done_ids)} done)" if done_ids else ""))
        raw_path = os.path.join(raw_dir, f"{run_id}_{log_name(framing, readings).replace('run_log_lab_', '')}.jsonl")
        with open(out, mode, newline="", encoding="utf-8") as f, open(raw_path, "w", encoding="utf-8") as raw:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            if mode == "w":
                w.writeheader()
            for i, it in enumerate(queue, start=len(done_ids) + 1):
                ep = run_episode(it, framing, noisy, key, raw, max_tokens=args.max_tokens,
                                 domain=args.domain, model=args.model)
                T = int(it["test_t"])
                if args.domain == "freefall":
                    cf, real = fmt(float(it["coefficient"]) * T ** int(it["exponent"])), fmt(4.9 * T * T)
                else:  # the Standard run's answer key: exact law, and the familiar form fitted to the 6 table points
                    cf = fmt(float(it["coefficient"]) * (int(it["test_x"]) / D["scale"]) ** float(it["exponent"]))
                    real = it.get("real_answer", "")
                w.writerow({
                    "run_id": run_id, "call_index": i,
                    "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    "item_id": it["item_id"], "framing": framing, "readings": readings,
                    "law_distance": it["law_distance"], "law_variant": it["law_variant"],
                    "formula": it["formula"], "test_t": T, "prompt_id": D["framings"][framing]["prompt_id"],
                    "model": M["model"], "quantization": M["quant"] or "n/a", "temperature": 0.0,
                    "seed": 0 if M["seed"] else "none",
                    "max_tokens": args.max_tokens, "reasoning_setting": "off",
                    "cf_answer": cf, "real_answer": real,
                    "domain": args.domain, "test_x": it.get("test_x") or T,
                    **ep,
                })
                f.flush()
                print(f"  [{i}] {it['item_id']}: {ep['n_measurements']} measurements, {ep['n_turns']} turns, "
                      f"{ep['done_reason']}, {ep['provider']}")
                time.sleep(2)
        print(f"Wrote {len(queue)} episodes to {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
