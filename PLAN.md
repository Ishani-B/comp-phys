# Final plan: Starter

**Project:** Counterfactual Testing of How Language Models Weigh In-Context Evidence Against Memorized Training Knowledge

Locked 18 November 2026, before any model output was collected. The grading rule
below is not changed after seeing results.

- **What I change:** how far the law in the data is from real physics (real, near, far)
- **What I measure:** a normalized score, (prediction − counterfactual answer) / (real answer − counterfactual answer). 0 means it followed the data and 1 means it gave the real-world answer.
- **What stays the same:** the 6 data points shown, the prompt wording, the answer format, and a new chat for every call
- **Model:** Gemma 3 1B, local, through Ollama. Exact version: `gemma3:1b`, digest `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c` (instruction-tuned, 999.89M parameters, Q4_K_M quantization), Ollama 0.40.16. The run log records this on every row.
- **Randomness:** temperature 0. Later I rerun a small subset at the default temperature as a consistency check.
- **Grading rule:** I take the number after "Answer:". Tracked is a score of 0.2 or less, leaked is 0.8 or more, and anything in between I record as its exact score. "Called out" means the model says the data doesn't match real physics, and "hedge" means no number. Real-law items have no gap to divide by, so I score them by percent error, with within 5% counting as correct.
- **Prediction:** near-counterfactual data gets tracked, and far-counterfactual data pulls answers back toward real physics. If all three distances score the same, I'm wrong.

## Starter design

1 domain (free-fall) × 3 law distances (real, near, far) × 10 test predictions × 1 run = 30 calls. The real-law condition runs first: it checks whether the model can do the extrapolation at all, apart from memorization.

- Data: [`data/freefall_starter.csv`](data/freefall_starter.csv), declared in [`data/DATA.md`](data/DATA.md)
- Prompt: `P1` in [`prompts/prompts.md`](prompts/prompts.md)

## Details fixed while writing the scripts, before running

These were not spelled out in the plan above. I fixed them before any output was collected.

1. **Which "Answer:" counts.** If "Answer:" appears more than once, the last one counts. The number is the first one on the rest of that line (or the next line if that line is empty). Commas are removed, so "1,024" is 1024. No "Answer:" anywhere, or no number after it, is a hedge, and the run log records which (`no_answer_line` or `non_numeric`).
2. **Scores outside 0 to 1.** The rule is applied as written, so a score of −3 counts as tracked and 1.6 counts as leaked. Every such score is also flagged in an `outside_0_1` column and counted in the summary, so they are visible.
3. **Called out is a flag, not a replacement for the score.** A called-out answer that still gives a number is scored by that number (I am scoring the answer, not the reasoning). Called out is coded by reading every response, stored in [`results/called_out_coding.csv`](results/called_out_coding.csv), and counted separately.
4. **Rounding.** Normalized scores are rounded to 4 decimal places and labelled from the rounded value, so a score of 0.79999 is recorded and labelled as 0.8.
5. **Generation settings.** Seed 0, at most 1024 output tokens per call, no system prompt. A response cut off at 1024 tokens is marked `length` in the `done_reason` column.

## Changes after starting

**18 November 2026, after the first 10 real-law calls, before any near or far call.** The output cap (detail 5) was 1024 tokens. In that first real-law run, 7 of 10 responses were cut off at the cap before reaching an "Answer:" line, which would score them as hedges. Reading them showed the model had already computed the correct value (for example, it found d = 4.9t² and 396.9 at 9 seconds), then kept re-deriving ("However, this is not an integer. Let's try a different approach") until it ran out of tokens. The cut-offs came from my cap, not from the model declining to commit. I raised the cap to 4096 tokens and reran the real-law condition, then ran near and far at 4096 too. The grading rule is unchanged. The first run is kept as `results/run_log_gemma3-1b_cap1024_real.csv` and scored separately. At temperature 0 the outputs are deterministic: each of the 10 capped responses is, character for character, the start of the matching 4096-token response, so raising the cap only let responses finish and changed nothing else.

**18 November 2026, model corrected to Gemma 4 31B, before any 31B call.** The plan's model is "Gemma 31B", which is Gemma 4 31B. It was first misread as a typo for Gemma 3 1B, and the 30 calls above ran on Gemma 3 1B. Those results are kept as their own run (`results/run_log_gemma3-1b*`). Gemma 4 31B (19 to 20 GB) does not fit on this Mac (16 GB memory, 11 GB free disk), so it runs through OpenRouter instead of locally:

- Model `google/gemma-4-31b-it`, pinned to one provider (Crusoe, bf16 weights) with fallbacks to other providers turned off, so every call uses the same weights. The provider and the model version OpenRouter reports are recorded on every row.
- Temperature 0, seed 0, at most 4096 output tokens, a new chat for every call, no system prompt: the same settings as the final Gemma 3 1B run.
- Reasoning (Gemma 4's optional thinking mode) off. The plan does not mention it, and Gemma 3 1B has none, so this keeps the two runs comparable.
- Same data file, same prompt `P1`, same grading rule. The real-law condition runs first.
- Temperature 0 on a hosted provider is not guaranteed to be deterministic the way it was locally, so a rerun may not match character for character.

## Pilot: harder evidence (locked 18 November 2026, before any pilot call)

**Why.** In the Starter, Gemma 4 31B scored exactly 0 on every counterfactual item. Six exact points make any law easy to read off, so there was no gradient to see. This pilot weakens the evidence to find out whether the pull toward real physics appears once the data are less clear.

**What changes:** only the evidence. Everything else is the Starter: the same 30 laws and test times, `google/gemma-4-31b-it` on Crusoe (bf16), prompt `P1`, temperature 0, seed 0, at most 4096 output tokens, reasoning off, a new chat for every call.

| Evidence level | Points shown | Data file |
|---|---|---|
| Noisy | six points, t = 1 to 6. Each value multiplied by a random factor between 0.9 and 1.1 (±10%), then rounded to one decimal. Fixed seed. Every law distance uses the same noise factors at the same test time, so the law is still the only difference between conditions. | `data/freefall_pilot_noisy.csv` |
| Sparse | three exact points, t = 1 to 3 | `data/freefall_pilot_sparse.csv` |

30 items × 2 levels = 60 calls. Real-law items run first within each level.

**Scoring:** the locked grading rule, unchanged. Correct answers come from the noise-free law that generated each table.

**Recorded but not scored:** two more reference answers per item, computed from the points shown. `t2_fit_answer` is d = k·t² with k fitted by least squares, the real law's shape with a constant taken from the data. `quad_fit_answer` is a least-squares fit of a·t² + b·t + c. Each answer is also marked with whichever reference it is closest to: the data's law, the real law, the t² fit or the quadratic fit. This separates "kept the familiar shape" from "recalled Earth's constant".

**Prediction, from the main hypothesis:** with weaker evidence, far-counterfactual scores rise above near-counterfactual scores. If every score stays at 0, the ceiling holds even with weaker evidence.

## Virtual lab (approved and locked)

*Written and approved 18 November 2026. Locked the same evening after the mechanics check (below) and before any of the 120 real episodes. Code: [`scripts/lab.py`](scripts/lab.py), tested by [`tests/test_lab.py`](tests/test_lab.py). Prompts: `P2` and `P3` in [`prompts/prompts.md`](prompts/prompts.md).*

### Why

The Starter and the pilot hand the model a finished table. Here the model gathers its own evidence: it is placed in a world with its own law, chooses which measurements to take, sees each result, decides when it knows enough, and then predicts a time it never measured. The research question is unchanged: when a model runs its own experiments, does it follow the law in its data or fall back on real physics? The pilot found the pull shows up when evidence is noisy, and as the familiar t² shape rather than Earth's constant. The lab tests whether that holds when the model controls the evidence, and lets us watch how it experiments: which times it picks, whether it tests ½gt² first, and when it stops.

### Goals, non-goals, anti-goals

- **Goal:** the same answer scored the same way (locked grading rule), so lab results line up with the Starter and pilot; plus a record of how the model experimented.
- **Goal:** a framing control. The same law, once as a falling-ball story and once with made-up names and no physics cues. The gap between the two measures how much the physics story pulls.
- **Non-goal:** measuring general scientific ability, or open-ended discovery of several laws at once (the "open sandbox", not chosen).
- **Anti-goal:** a lab where the model can measure the answer directly. Measurements stop at 6 seconds; predictions are at 7 to 16 seconds.
- **Anti-goal:** readings the model invents. With built-in tool calling the model must wait for each real result.

### Approaches considered

| Approach | Trade-off | |
|---|---|---|
| **Built-in tool calling:** the model calls a measurement tool and the script returns each reading | Structured, no invented readings, the budget is enforced by the script, works for Claude through OpenRouter too. Needs a model and provider with tool support (Crusoe has it). | **Chosen** |
| Text commands: the model writes `MEASURE 3.5`, the script replies | Works with any model, including small local ones; needs fragile parsing, and models sometimes write fake readings after the command | Not chosen |
| One-shot plan: the model lists all measurements up front, then answers | Simplest, but it can't adapt, so it isn't really running experiments | Dropped |

### Decided by you

- A virtual lab for the same laws (not an open sandbox).
- The model runs its own experiments.
- Built-in tool calling.

### Design (Claude's calls; correct anything)

**Model and settings.** `google/gemma-4-31b-it` through OpenRouter, pinned to Crusoe (bf16) with no fallback, temperature 0, seed 0, at most 4096 output tokens per model turn, reasoning off, tool choice left to the model (`auto`). The same settings as the Starter and pilot.

**Laws and targets.** The Starter's 30 laws (10 real, 10 near, 10 far) and their test times, T = 7 to 16. One episode per law per condition, asking about that law's T.

**Conditions.** 2 readings × 2 framings:

| | Exact readings | Noisy readings (±10%) |
|---|---|---|
| **Physics framing** | 30 episodes | 30 episodes |
| **Neutral framing** | 30 episodes | 30 episodes |

120 episodes in all. Run order: physics-exact, physics-noisy, neutral-exact, neutral-noisy; within each cell, real, then near, then far.

**What the model is told (one user message, no system prompt).**

- *Physics framing (prompt `P2`):* "You are in a lab on a planet. You can drop a ball and measure how far it has fallen, in meters, after any time you choose between 0 and 6 seconds, using the `drop_ball` tool. You have up to 8 measurements. Your goal: work out how far the ball will have fallen after T seconds. When you're done measuring, state the rule you found, then end with 'Answer: X'."
- *Neutral framing (prompt `P3`):* the same structure and wording, with every physical cue replaced. A device has a dial and a counter: set the dial to any number of "tocks" between 0 and 6 and read how many "glims" the counter shows, using the `read_counter` tool. The goal is the number of glims at T tocks. No words like ball, drop, fall, planet, seconds, meters, gravity.
- The exact wording of both prompts and both tool descriptions is recorded in `prompts/prompts.md` before any call.

**The tool.** One argument, the time (seconds or tocks), any number with 0 < t ≤ 6, rounded to 2 decimals. It returns the reading rounded to 3 decimals: `{"seconds": 2.5, "meters": 30.625}`, or `{"tocks": 2.5, "glims": 30.625}` in the neutral framing.
- *Exact:* the law's value.
- *Noisy:* the law's value times a factor drawn uniformly from [0.9, 1.1]. Every reading gets its own factor, so repeating a measurement gives a new value, as with a real instrument. **The noise is matched across conditions** (Claude's call, after the design review): the factor for the nth valid reading depends only on the test time T and n, from a fixed seed. Physics and neutral episodes for the same law therefore get the same noise sequence, and so do the real, near and far laws that share a T. This follows the pilot, so the law and the framing stay the only differences. With 10 episodes per cell, unmatched noise could otherwise create a "framing effect" by luck. A rerun returns the same readings for the same requests.
- *Out of range* (t ≤ 0 or t > 6): an error message, "Only times between 0 and 6 are possible". It does not use up a measurement.
- *Budget spent:* after 8 valid measurements every further call returns "No measurements left. Give your answer."
- *Several calls in one turn* are each answered, in order, and each counts.

**Ending an episode.** It ends when the model replies without a tool call. The answer is the number after "Answer:", parsed exactly as in the Starter. Safety caps: at most 12 model turns per episode. An episode that hits the cap, or ends with no number, is a hedge. Answering without any measurement is allowed and recorded.

**Scoring (locked rule, unchanged).** Normalized score for near and far, percent error for real (within 5% is correct), hedge for no number, called out coded by hand by the same rule as the Starter. In the neutral framing "called out" is not applicable (there is no physics to call out); any mention of physics there is recorded as notable.

**Recorded per episode (descriptive, not scored).**
- Every time requested, in order, and every reading returned.
- Number of measurements used, and how many were repeats.
- The rule the model stated.
- Whether its first stated or tested hypothesis was the t² form (coded by hand, like called out).
- Whether the reply mentions real physics.
- The t² fit and the quadratic fit of the readings it actually got, as in the pilot, and which reference the answer lands closest to.

**Prediction, from the main hypothesis.** Far-counterfactual scores rise above near, more with noisy readings than exact ones, and more in the physics framing than the neutral one. If the physics and neutral framings score the same at every distance and noise level, the physics story isn't pulling the answers.

**How the prediction is judged** (Claude's call, after the design review; fixed before any lab call):
- *Primary outcome:* the locked one. The mean normalized score per cell (framing × readings × law distance), with the median and the counts of tracked, between, leaked, hedge and called out beside it, as in the Starter.
- *Second pre-registered measure:* for every near and far episode, which reference the answer lands closest to (the data's law, Earth's law 4.9·T², the t² fit or the quadratic fit of the readings the model actually got), using the pilot's rule. This separates a fallback to the familiar t² shape from a recall of Earth's numbers.
  - This matters most for the framing comparison. In the neutral framing, Earth's answer has no meaning, so a high normalized score there can only be a shape fallback.
  - The physics story counts as pulling toward real physics only if physics-framing answers land closest to Earth's law more often than neutral-framing answers do.
- *Exploratory, not confirmatory.* With 10 episodes per cell, results are reported as directions and counts, with no significance claims. The exact-reading cells may all score 0, as on clean data before, in which case the comparison rests on the noisy cells, and that is reported as such.

### Before locking: mechanics check

Before the design is locked, 8 unscored test episodes check the machinery. They use two laws that are not among the 30: d = 6·t² asked at T = 9, and d = 0.8·t³ asked at T = 12. Each runs in both framings with exact and noisy readings.
- *What they check:* the model calls the tool rather than writing calls as text, the budget and window rules work, transcripts parse, and the "Answer:" line is found.
- *What they don't do:* reveal anything about the 120 real episodes. They are saved under `results/lab_smoke/` and left out of every analysis.
- *If tool calling doesn't work* with this model on Crusoe, Claude stops and asks, rather than switching provider or method.

**Mechanics check, done 18 November 2026.** The first attempt failed on its first episode: the model asked for two measurements at once, the provider merged them into one malformed call (`{"seconds": 1}{"seconds": 2}`), and the provider then rejected the conversation when it was sent back.
- *Fix (mechanics only, matching the design's "several calls in one turn are each answered, in order, and each counts"):* merged calls are split into separate valid calls, each answered and counted. How often it happens is recorded per episode (`n_merged_calls`). The failed attempt was discarded and the check rerun.
- *Rerun:* all 8 episodes ran, the model used the tool in both framings, every reply parsed, and the budget and window rules held. Merged calls happened in every episode and were handled.
- *Token limit:* one episode (neutral, noisy) wandered in its final message past the 4096-token limit and counts as a hedge. That is the same limit and the same outcome as in the pilot, so the limit is unchanged.
- No other change. The check cost $0.0065, about 1 minute per episode.

**Run arrangement.** To halve the wall-clock time, the physics cells (exact, then noisy) and the neutral cells (exact, then noisy) run as two parallel streams. Within each cell the order is real, near, far. Episodes are independent, so the order does not affect results.

**During the real run (18–19 November 2026).**
- *Rate-limit crash:* the neutral stream hit a long stretch of provider rate-limiting and stopped after 25 neutral-exact episodes, with no row written for the episode in progress. The stream went on to the neutral-noisy cell.
- *Resume:* the 5 unrun far episodes (FF-F-06 to FF-F-10) were run afterwards under a new run ID (`20261119T004110Z`) with more patient retries (up to 20). No finished episode was repeated. The partial attempt at FF-F-06 stays in that stream's raw JSONL and is not part of any result.
- *Run-time physics-word flag:* the `physics_words` column flagged a bare "9.8", which also matched ordinary numbers like 19.8. `compare_lab.py` recomputes physics mentions with a stricter pattern, and that is the number reported. No neutral reply mentions physics.

### Supplementary rerun: token-limited episodes (pre-registered 19 November 2026, before any rerun call)

**Why.** 19 of the 60 noisy episodes ended without an answer because the model's final message hit the 4096-token limit: 5 physics (FF-R-03, FF-R-07, FF-N-10, FF-F-01, FF-F-10) and 14 neutral (FF-R-02, FF-R-03, FF-R-06, FF-R-09, FF-R-10, FF-N-03, FF-N-06, FF-N-08, FF-N-09, FF-N-10, FF-F-01, FF-F-02, FF-F-05, FF-F-09). Hedges are uneven across framings, so whether those episodes would have answered could change the framing comparison.

**What.** Exactly these 19 episodes are rerun from the start with the per-turn output limit raised from 4096 to 16384 tokens. Everything else is unchanged: same model, provider, settings, prompts, tool and matched noise, so the same requests get the same readings. Each episode runs once, under a new run ID, into separate logs (`results/run_log_lab_<framing>_noisy_cap16k.csv`).

**How it is reported.**
- The 4096 results stay the primary, pre-registered result.
- The rerun is reported beside them as a supplementary check: how many of the 19 now answer, how those answers score, and what each noisy cell looks like if rerun answers replace the hedges.
- Hosted temperature 0 is not guaranteed to repeat exactly, so a rerun may take a different path before its final message. That is reported too.
- No other episode is rerun.

**During the rerun (19 November 2026).**
- *Hung requests:* after 2 episodes each, both streams hung for about two hours on a single request (FF-N-10 physics, FF-R-06 neutral). The connection was open but no response came, and urllib's timeout only bounds silence between chunks, so it never fired.
- *Fix (mechanics only):* both processes were stopped. Every request now has a hard 15-minute overall deadline and is retried if it is hit.
- *Resume:* the 4 finished rerun episodes are kept. The two hung ones never finished, so they rerun from the start along with the rest.

### If something breaks during the real run

A mechanical problem found during the real episodes, such as a cap set too low, is fixed with a dated entry under "Changes after starting", like the Starter's token cap. Affected episodes are rerun under a new run ID, the originals are kept, and both are reported.

**Logging.**
- **Run log:** one row per episode, with the full transcript (every model turn, tool call and reading) in the output column, plus all the per-call metadata the Starter logs (provider, tokens, cost, finish reasons).
- **Raw record:** every API request and response in a JSONL file per run, so any episode can be replayed.
- **Drive log:** the lab's standard columns, one row per episode. Note in each row's notes that an episode contains several model calls.

**Cost and time.** About 120 episodes × up to 9 model turns, roughly $1 and under an hour at Crusoe's rate limits.

### Left to the builder

Code structure, retry and resume behaviour (same as `run_openrouter.py`: never repeat a finished episode), the exact JSON shape of tool messages, and how the transcript is rendered as text.

## Reproduce

```bash
python3 scripts/generate_items.py      # writes data/freefall_starter.csv
python3 scripts/check_items.py         # recomputes the answer key
python3 -m unittest discover tests     # tests the answer parser and grading rule
ollama serve                           # in another terminal
python3 scripts/run_ollama.py --model gemma3:1b --conditions real --num-predict 4096
python3 scripts/run_ollama.py --model gemma3:1b --conditions near far --append --num-predict 4096
python3 scripts/score.py results/run_log_gemma3-1b.csv

# Gemma 4 31B through OpenRouter (key in .env as OPENROUTER_API_KEY; .env is never committed)
python3 scripts/run_openrouter.py --conditions real
python3 scripts/run_openrouter.py --conditions near far --append
python3 scripts/score.py results/run_log_gemma-4-31b-it.csv
```
