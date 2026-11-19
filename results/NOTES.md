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

## Pilot: harder evidence (Gemma 4 31B)

Same 30 laws and test times, same settings. Only the evidence changes. Design: "Pilot: harder evidence" in `PLAN.md`. Tables: [`pilot_evidence_comparison.md`](pilot_evidence_comparison.md). Cost $0.0175 for 60 calls.

| Evidence | Real-law control | Near: mean score | Far: mean (median) | Far tracked | Hedges | Called out | Replies invoking real physics |
|---|---|---|---|---|---|---|---|
| Exact, 6 points (Starter) | 10/10 | 0.00 | 0.00 (0.00) | 10/10 | 0 | 0 (2 borderline) | 5/30 |
| Noisy (±10%), 6 points | 9/10 | 0.03 | 0.19 (0.00) | 8/10 | 1 | 1 (9 borderline) | 30/30 |
| Exact, 3 points | 10/10 | 0.00 | 0.00 (0.00) | 10/10 | 0 | 0 (2 borderline) | 14/30 |

**Noise moves the model; fewer points don't.** With three exact points the model was perfect again, picking t³ from just three cubic points every time. With noisy points, far items slip: one leaked and one hedged.

**The direction matches the prediction, but weakly.** Under noise the far mean (0.19) sits above the near mean (0.03), as the hypothesis predicts. But the far mean rests on one item, and both medians are about 0. Ten items per cell can't call this a real effect.

**The only leak is a pull toward the familiar shape, not Earth's numbers.** In FFNZ-F-09 (true law d = 0.5t³) the model tries a cubic close to the truth (0.45t³ gives 1518.75), then drops it for a quadratic and answers 612.3. That is closest to the t² fit of the points (574), not to Earth's answer (1102.5). The normalized score calls it "leaked" (1.84, outside 0 to 1) because it only measures distance from the data's answer toward Earth's. No far answer at any evidence level is closest to Earth's answer.

**Noise is what brings the physics in.** With clean data the model mentions real physics in 5 of 30 replies. With noise it does in 30 of 30: almost every reply opens "In physics, the distance an object falls under constant gravity is d = ½gt²". It then blames deviations on "measurement error", and on near items it uses the physics as a tie-breaker ("typically these problems follow d = kt²", "the t² relationship is the standard for falling objects"). Replies are about 2.5 times longer (median 910 tokens vs 391). On near items the prior agrees with the data, so it does no harm. On the 5 cubic items it conflicts: one ended on the t² shape and one ran out of tokens switching between polynomial fits.

**The failures are all cubic.** All 5 linear far items stayed tracked under noise (one drifted toward the quadratic fit: 142.1 vs 108, score 0.12). Both failures were among the 5 cubic items.

**Called out.** One clear call-out (FFNZ-F-05: the data are "inconsistent for a standard physics problem"). Nine noisy far replies test ½gt², find it doesn't fit and move on; they are coded borderline, the same rule as the Starter. All quoted in `called_out_coding.csv`.

**What it suggests next.** The pull toward real physics shows up when the evidence is ambiguous, and as a familiar shape rather than a recalled constant. A cleaner test would raise the noise in steps (5%, 10%, 20%, 40%) on cubic and other non-t² laws, and score against the t² fit as well as Earth's answer.

## Virtual lab: the model runs its own experiments (Gemma 4 31B)

Design: "Virtual lab" in `PLAN.md` (locked before the run). 120 episodes: the Starter's 30 laws × 2 framings (falling ball / made-up "tocks" and "glims") × 2 kinds of reading (exact / ±10% noise, matched across conditions). The model gets a measurement tool for 0 to 6 seconds, up to 8 measurements, then predicts T = 7 to 16. Full tables: [`lab_comparison.md`](lab_comparison.md). Cost $0.094. Coding: [`lab_coding.csv`](lab_coding.csv).

| Framing | Readings | Real-law control | Near mean | Far mean (median) | Far tracked | Hedges | Called out | Mean measurements | Mentions real physics | Far: tests t² first |
|---|---|---|---|---|---|---|---|---|---|---|
| Physics | exact | 10/10 | 0.00 | 0.00 (0.00) | 10/10 | 0 | 0 | 3.0 | 0/30 | 3/10 |
| Physics | noisy | 4/10 | 0.00 | 0.13 (0.01) | 7/10 | 5 | 5 (+3 borderline) | 4.9 | 28/30 | 8/10 |
| Neutral | exact | 10/10 | 0.00 | 0.00 (0.00) | 10/10 | 0 | n/a | 3.7 | 0/30 | 2/10 |
| Neutral | noisy | 3/10 | −0.01 | 0.02 (0.01) | 6/10 | 14 | n/a | 6.1 | 0/30 | 0/10 |

**Exact readings are a ceiling in both framings.** Running its own experiments, the model typically measures at 1, 2 and 3 seconds (merging them into one turn), reads off the law and is exactly right: 60 of 60 episodes, cubics included.

**Noisy readings break the control, more than a noisy table did.** With a noisy table (pilot) the real law was right 9/10 times. In the lab it is 4/10 (physics) and 3/10 (neutral). Two reasons:
- The model rarely repeats a measurement to average out noise (4 of 60 noisy episodes). It spreads its readings across times and fits the noise.
- Its final message often keeps re-fitting until it hits the 4096-token limit without an answer. All 19 noisy hedges are this; none hit the turn cap.

Because the control fails under noise, the noisy cells' counterfactual scores are weak evidence either way.

**The physics story sets the first guess.** With noisy readings, 8 of 10 far episodes in the physics framing open by testing ½gt² ("The distance a ball falls under constant gravity is d = ½gt²"). In the neutral framing, 0 of 10 do; it starts from differences or polynomial fits. With exact readings the gap is small (3/10 against 2/10, all on cubic laws), because the data settle it at once. No neutral reply mentions physics at all.

**It also changes how much evidence the model gathers and whether it commits.**
- *Measurements:* the physics framing takes fewer (3.0 against 3.7 exact, 4.9 against 6.1 noisy).
- *Commitment:* with noise, the physics framing commits to an answer far more often (5 hedges against 14). With a familiar law to fall back on, it settles. Without one, it keeps fitting.
- *On cubic laws with noise:* physics tracked 2, leaked 1, hedged 2; neutral tracked 1, hedged 4.
- *On linear laws:* both framings tracked 5/5.

**The one leak is a shape default, not Earth's numbers.** FF-F-05 (true law t³), physics framing, noisy: the model starts "proportional to the square of the time", takes only 3 readings, and answers 572.5, exactly the quadratic through its three noisy points. That happens to sit near Earth's 592.9, so the normalized score says "leaked" (1.03). The second measure says otherwise: it lands closest to the quadratic fit. **No near or far answer in any of the four cells lands closest to Earth's law.**

**Called out, only with noise and only on linear laws.** Five physics-framing far replies say outright that the data don't fit standard physics: "This is not a standard gravity problem", "inconsistent with a standard gravity formula", "the environment is not a simple constant-gravity vacuum or there is noise". All five are linear laws (d = c·t), where ½gt² fails visibly. On the cubic laws the model tests ½gt², drops it and moves on without comment (3 borderline).

**Against the pre-registered prediction.**
- *Far above near:* holds directionally in the physics-noisy cell (0.13 against 0.00), resting on one episode.
- *Noisy above exact:* holds. Exact is a ceiling, and noise is the only place anything moves.
- *Physics above neutral:* holds directionally on the locked mean (0.13 against 0.02). But by the pre-registered rule the physics story counts as pulling toward real physics only if physics-framing answers land closest to Earth's law more often than neutral ones, and that count is 0 against 0. So: **not supported as a pull toward real physics.** What the framing does change is the model's first hypothesis, how much evidence it gathers, and whether it commits.
- With 10 episodes per cell this is exploratory.

**Supplementary rerun of the 19 token-limited episodes at 16,384 tokens.** Pre-registered in `PLAN.md`. The 4096 results above stay primary. Cost $0.066. Full table: "Supplementary" in [`lab_comparison.md`](lab_comparison.md).

17 of the 19 now answer (2 neutral ones ran past even 16,384). Several needed 8,000–16,000 tokens, so the 4096 limit was cutting off real answers.

| Noisy cell, hedges replaced by rerun answers | Real-law control | Near tracked | Far: mean (median) | Far tracked | Hedges left |
|---|---|---|---|---|---|
| Physics | 6/10 (was 4/10) | 8/10 | 0.12 (0.01) | 9/10 (was 7/10) | 0 |
| Neutral | 5/10 (was 3/10) | 9/10 (was 5/10) | 0.05 (0.01) | 8/10 (was 6/10) | 2 |

- **The hedges mostly hid answers, not failures.** With room to finish, both framings track far laws 8–9 times in 10, and both controls rise to about half. The hedge gap between framings (5 against 14) was largely a token-limit effect: without a familiar law to anchor on, the neutral framing reasons longer, and with more room it mostly gets there.
- **No real framing difference in accuracy remains.** Control 6/10 against 5/10. The far means (0.12 against 0.05) still rest on the single physics "leak", the quadratic through three noisy points.
- **Still no recall of Earth's numbers.** One rerun (physics FF-N-10, true law 1.2t²) is the first answer in the project that the pre-registered measure places closest to Earth's law. Its reasoning shows why that's misleading: it opens with ½gt², takes g ≈ 2.2 from the data (never 9.8), then overfits the noisy readings with d = t² + 0.08t³ and answers 583.7. That is 53% off Earth's answer and 90% off the data's. It counts as "closest to Earth" only because distance is measured in relative terms.
- **Reruns take different paths.** Hosted temperature 0 is not deterministic: some reruns answered in under 4096 tokens (physics FF-R-03 used 1,932) where the original ran past the limit.

**Net result of the lab, with the rerun:** the physics story changes how the model experiments (its first guess, how much it measures, how quickly it commits) but not where it ends up. When the model controls its own evidence, it follows the world's law, not real physics, as long as it has room to finish reasoning.

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
