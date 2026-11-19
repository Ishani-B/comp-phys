# Lab extension: Hooke's law, both models

Design: "Lab extension" in `PLAN.md`. Each model chooses its own weights (0–600 g, up to 8), then predicts the stretch at 700–1600 g. Normalized score: 0 = the data's law, 1 = the straight line fitted to the Standard's table points. 10 items per row.

## Locked outcome

| Model | Framing | Real-law control | Near: mean (median) | Near tracked / between / leaked / hedge | Far: mean | Far tracked | Called out |
|---|---|---|---|---|---|---|---|
| Gemma 4 31B | spring story | 10/10 | 0.06 (0.00) | 7/2/0/1 | 0.00 | 10/10 | 2 |
| Gemma 4 31B | neutral dial | 10/10 | 0.15 (-0.01) | 8/0/2/0 | 0.00 | 10/10 | n/a |
| Claude Sonnet 4.6 | spring story | 10/10 | 0.03 (0.01) | 9/1/0/0 | 0.00 | 10/10 | 19 |
| Claude Sonnet 4.6 | neutral dial | 10/10 | -0.22 (0.00) | 8/0/0/2 | -0.02 | 10/10 | n/a |

## The same near laws: given a table vs choosing the measurements

| Model | Setting | Near: mean (median) | Near tracked / between / leaked / hedge |
|---|---|---|---|
| Gemma 4 31B | Standard: table of 6 points | 0.12 (0.15) | 5/4/1/0 |
| Gemma 4 31B | Lab: spring story | 0.06 (0.00) | 7/2/0/1 |
| Gemma 4 31B | Lab: neutral dial | 0.15 (-0.01) | 8/0/2/0 |
| Claude Sonnet 4.6 | Standard: table of 6 points | -0.18 (-0.16) | 10/0/0/0 |
| Claude Sonnet 4.6 | Lab: spring story | 0.03 (0.01) | 9/1/0/0 |
| Claude Sonnet 4.6 | Lab: neutral dial | -0.22 (0.00) | 8/0/0/2 |

## How they measured, and where near answers land

| Model | Framing | Mean measurements | Widest weight measured (median) | Replies naming Hooke's law | Near answers closest to: data law / straight line / quadratic / other |
|---|---|---|---|---|---|
| Gemma 4 31B | spring story | 3.9 | 400 g | 2/30 | 9 / 0 / 0 / 1 |
| Gemma 4 31B | neutral dial | 4.3 | 400 g | 0/30 | 6 / 2 / 1 / 1 |
| Claude Sonnet 4.6 | spring story | 6.4 | 600 g | 30/30 | 9 / 0 / 0 / 1 |
| Claude Sonnet 4.6 | neutral dial | 6.6 | 600 g | 0/30 | 7 / 0 / 1 / 2 |

Lab extension cost $1.6397.

