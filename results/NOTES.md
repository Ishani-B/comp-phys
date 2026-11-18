# Starter run: notes

Run 18 November 2026. These notes come from reading every response (written up by Claude, for checking). The plan's model is Gemma 4 31B. An earlier run used Gemma 3 1B by mistake; it is kept below as a second, smaller model.

## Files

| File | What it is |
|---|---|
| `run_log_gemma-4-31b-it.csv` (+ `_scored.csv`, `_summary.md`) | **The Starter run.** Gemma 4 31B through OpenRouter, provider Crusoe (bf16), 30 calls, one row per call with the full response. Total cost $0.0049. |
| `run_log_gemma3-1b.csv` (+ scored, summary) | Gemma 3 1B, local through Ollama, 30 calls, 4096-token cap |
| `run_log_gemma3-1b_cap1024_real.csv` (+ scored, summary) | Gemma 3 1B's first real-law run at a 1024-token cap, kept as a record. See "Changes after starting" in `PLAN.md`. |
| `called_out_coding.csv` | Hand coding of "called out" for every call in every run, with quotes where relevant |

## Gemma 4 31B (the Starter run)

| Condition | Result |
|---|---|
| Real-law control | 10/10 exactly right |
| Near (changed constant) | 10/10 tracked, every score exactly 0.0 |
| Far (changed exponent or form) | 10/10 tracked, every score exactly 0.0 |
| Hedges | 0 |
| Called out | 0 (2 borderline, below) |

**Every one of the 30 answers is exactly the value the data's own law gives.** All 30 calls went to the same provider and finished on their own, with no reasoning tokens.

**The model knows the real law and drops it when the data disagree.** On three real-law items it names d = 4.9t² as "the standard formula for distance fallen under gravity" with g = 9.8. On two cubic items (FF-F-09, FF-F-10) it first tests "the formula for free fall, d = ½gt²", sees that d/t² is not constant, and switches to t³. So the memorized law is the first thing it tries, and the data overrule it every time.

**Borderline "called out" (FF-F-09, FF-F-10).** Those two responses imply the data don't follow the free-fall formula, but they never say anything is wrong or unusual; they just move on to the next hypothesis. The plan defines called out as "says or implies that the data doesn't match real physics". They are coded `borderline`, not counted, and quoted in `called_out_coding.csv`, so you can decide.

**Against the hypothesis.** The plan says: "If all three distances score the same, I'm wrong." For free-fall on Gemma 4 31B they do: near and far both average 0.00, and the real-law control is 10/10. On this domain and this model, the prediction that far-counterfactual data pulls answers back toward real physics is not supported. The Starter covers one domain only, so this doesn't speak to Hooke's law or Kepler's third law yet.

**Ceiling, not a gradient.** With every score at 0, the Starter can't show *how* fallback grows with distance, because there is no fallback to measure. The data are noise-free and fit simple formulas exactly (six points, clean constants, whole-number exponents), which makes the counterfactual law as easy to read as the real one. Harder evidence, such as noisy points, fewer points, or a less familiar form, is where a difference between near and far could show up.

## Gemma 3 1B (earlier run, smaller model)

| Condition | Result |
|---|---|
| Real-law control | 4/10 correct (T = 7, 8, 10, 11); wrong for every T from 12 up |
| Near | 6 labelled tracked, but only 1 is the data-correct value; mean −7104.82 |
| Far, linear | 5/5 exactly right |
| Far, cubic | 0/5 right |
| Hedges / called out | 1 hedge (a loop that filled the context window) / 0 |

**The control fails.** The model often finds d = 4.9t² and computes the right value, then drops it: three times it ends "the next difference is 9.8, so d = 176.4 + 9.8 = 186.2", whatever T is. By the plan's own test, its counterfactual results tell us little.

**The rule labels wild answers as "tracked".** A score of 0.2 or less counts as tracked, and negative scores qualify. One answer of 37,748,736 (it decided d = 9 × 4^(t−1)) scores −63,935 and sets the near mean almost single-handedly. These scores are flagged in the `outside_0_1` column.

**Its far "leaks" are a shape default, not Earth physics.** On cubic tables it fits a quadratic through the first three points. No 1B counterfactual response mentions 4.9 or 9.8. One quadratic fit (611) happens to land near Earth's 592.9 and scores 0.98.

**Compared with 31B.** Both models reach for t² first. Gemma 3 1B can't get past it on cubic data, or do the arithmetic reliably; Gemma 4 31B checks it, rejects it, and fits the data exactly.

## Design issues found (to add to the README's Known issues)

- **"On a planet" makes the near condition real physics.** On another planet a different constant is real physics (d = ½gt² with that planet's g), so tracking a changed constant isn't going against anything memorized. Only the far condition is counterfactual in the strict sense. Gemma 4 31B tracked both perfectly, so it didn't matter here, but it matters for interpreting near.
- **The 0.2 / 0.8 cutoffs need a lower and upper bound** for the labels to mean "close to" one answer or the other. The locked rule is applied as written, and out-of-range scores are flagged rather than relabelled.
- **Two reference points can't capture a shape default.** A third reference answer, the best quadratic fit to the six points, would separate "kept the t² shape" from "recalled Earth's 4.9". This mattered for Gemma 3 1B.
- **Hosted temperature 0 is not guaranteed deterministic.** The 31B run went through a hosted provider, so a rerun may not match character for character. The plan's default-temperature consistency check covers this.
