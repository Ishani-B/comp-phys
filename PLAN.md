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
