# Standard run: three domains, two models

Design: "Standard run" in `PLAN.md`. Normalized score: 0 = followed the data's law, 1 = gave the real-world answer (Earth's law for free fall; the familiar form fitted to the data for Hooke and Kepler). 10 items per cell.

| Domain | Model | Real-law control | Near: mean (median) | Near tracked / between / leaked | Far: mean (median) | Far tracked / between / leaked | Hedges | Called out |
|---|---|---|---|---|---|---|---|---|
| Free fall | Gemma 4 31B | 10/10 | 0.00 (0.00) | 10/0/0 | 0.00 (0.00) | 10/0/0 | 0 | 0 (+2 borderline) |
| Free fall | Claude Sonnet 4.6 | 10/10 | 0.00 (0.00) | 10/0/0 | 0.00 (0.00) | 10/0/0 | 0 | 0 |
| Hooke | Gemma 4 31B | 10/10 | 0.12 (0.15) | 5/4/1 | 0.03 (0.00) | 9/1/0 | 0 | 1 (+2 borderline) |
| Hooke | Claude Sonnet 4.6 | 10/10 | -0.18 (-0.16) | 10/0/0 | 0.00 (0.00) | 10/0/0 | 0 | 0 |
| Kepler | Gemma 4 31B | 10/10 | -0.05 (0.00) | 10/0/0 | 0.00 (0.00) | 10/0/0 | 0 | 8 (+5 borderline) |
| Kepler | Claude Sonnet 4.6 | 10/10 | -0.13 (0.00) | 10/0/0 | 0.00 (0.00) | 10/0/0 | 0 | 0 (+9 borderline) |

New Standard calls cost $0.6533 (Gemma free fall reused from the Starter).

