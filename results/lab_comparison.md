# Virtual lab: Gemma 4 31B runs its own experiments

Normalized score: 0 = followed the world's law, 1 = gave Earth's answer. Real-law items: number correct within 5%. 10 episodes per row; exploratory, no significance claims.

## Locked outcome

| Framing | Readings | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Far leaked | Hedges | Called out |
|---|---|---|---|---|---|---|---|---|---|
| physics | exact | 10/10 | 0.00 (0.00) | 10/10 | 0.00 (0.00) | 10/10 | 0 | 0 | 0 |
| physics | noisy | 4/10 | 0.00 (0.00) | 8/10 | 0.13 (0.01) | 7/10 | 1 | 5 | 5 (+3 borderline) |
| neutral | exact | 10/10 | 0.00 (0.00) | 10/10 | 0.00 (0.00) | 10/10 | 0 | 0 | 0 |
| neutral | noisy | 3/10 | -0.01 (0.00) | 5/10 | 0.02 (0.01) | 6/10 | 0 | 14 | 0 |

## How it experimented

| Framing | Readings | Mean measurements | Episodes with repeats | Invalid calls | Merged calls | Mean turns | Replies mentioning real physics | Far: first hypothesis t² (read by hand) |
|---|---|---|---|---|---|---|---|---|
| physics | exact | 3.0 | 0/30 | 0 | 30 | 3.0 | 0/30 | 3/10 |
| physics | noisy | 4.9 | 4/30 | 0 | 42 | 4.5 | 28/30 | 8/10 |
| neutral | exact | 3.7 | 0/30 | 0 | 30 | 2.2 | 0/30 | 2/10 |
| neutral | noisy | 6.1 | 0/30 | 0 | 51 | 3.5 | 0/30 | 0/10 |

## Which reference near and far answers land closest to

Ties within 1% are joined with "=". For near laws the data's law, the t² fit and often the quadratic fit coincide, so the informative rows are far.

| Framing | Readings | Distance | data law | Earth's law | t² fit | quadratic fit | Ties / other | Hedge |
|---|---|---|---|---|---|---|---|---|
| physics | exact | near | 0 | 0 | 0 | 0 | 10 | 0 |
| physics | exact | far | 5 | 0 | 0 | 0 | 5 | 0 |
| physics | noisy | near | 2 | 0 | 3 | 2 | 2 | 1 |
| physics | noisy | far | 6 | 0 | 0 | 2 | 0 | 2 |
| neutral | exact | near | 0 | 0 | 0 | 0 | 10 | 0 |
| neutral | exact | far | 5 | 0 | 0 | 0 | 5 | 0 |
| neutral | noisy | near | 2 | 0 | 0 | 1 | 2 | 5 |
| neutral | noisy | far | 4 | 0 | 0 | 1 | 1 | 4 |

## Supplementary: token-limited episodes rerun at 16384 tokens

Pre-registered in `PLAN.md`. The 4096-token results above stay primary. These are the same episodes rerun from the start with a higher per-turn limit.

| Framing | Item | Law | Original | Rerun answer | Rerun label | Rerun score | Closest | Rerun measurements | Rerun output tokens | Finish |
|---|---|---|---|---|---|---|---|---|---|---|
| physics | FF-R-03 | d = 4.9 * t^2 | hedge | 411.48 | correct | 3.67 |  | 6 | 1932 | stop |
| physics | FF-R-07 | d = 4.9 * t^2 | hedge | 845 | correct | 2.04 |  | 5 | 3892 | stop |
| physics | FF-N-10 | d = 1.2 * t^2 | hedge | 583.68 | between | 0.2919 | Earth's law | 4 | 16443 | length |
| physics | FF-F-01 | d = 3 * t^3 | hedge | 994.1 | tracked | 0.0442 | data law | 6 | 8274 | stop |
| physics | FF-F-10 | d = 1.5 * t^3 | hedge | 5734.4 | tracked | 0.0838 | data law | 6 | 8199 | stop |
| neutral | FF-R-02 | d = 4.9 * t^2 | hedge | 288 | incorrect | 8.16 |  | 6 | 2937 | stop |
| neutral | FF-R-03 | d = 4.9 * t^2 | hedge | 412.5 | correct | 3.93 |  | 6 | 3280 | stop |
| neutral | FF-R-06 | d = 4.9 * t^2 | hedge | 720 | correct | 2.04 |  | 6 | 3493 | stop |
| neutral | FF-R-09 | d = 4.9 * t^2 | hedge | 336.457 | incorrect | 69.48 |  | 6 | 11388 | stop |
| neutral | FF-R-10 | d = 4.9 * t^2 | hedge | 886.4 | incorrect | 29.34 |  | 6 | 16468 | length |
| neutral | FF-N-03 | d = 7 * t^2 | hedge | none | hedge |  | hedge | 6 | 16468 | length |
| neutral | FF-N-06 | d = 9 * t^2 | hedge | 1200 | tracked | 0.1626 | t² fit | 6 | 9768 | stop |
| neutral | FF-N-08 | d = 12 * t^2 | hedge | 2254 | tracked | 0.0704 | t² fit | 6 | 1976 | stop |
| neutral | FF-N-09 | d = 3 * t^2 | hedge | 675 | tracked | 0.0 | data law | 6 | 1367 | stop |
| neutral | FF-N-10 | d = 1.2 * t^2 | hedge | 281.6 | tracked | -0.027 | data law = t² fit | 6 | 15088 | stop |
| neutral | FF-F-01 | d = 3 * t^3 | hedge | none | hedge |  | hedge | 6 | 16463 | length |
| neutral | FF-F-02 | d = 2 * t^3 | hedge | 947.2 | tracked | 0.1081 | data law | 6 | 2806 | stop |
| neutral | FF-F-05 | d = 1 * t^3 | hedge | 1331 | tracked | 0.0 | data law | 6 | 3359 | stop |
| neutral | FF-F-09 | d = 0.5 * t^3 | hedge | 1541.25 | between | 0.25 | data law | 6 | 9118 | stop |

### Noisy cells if rerun answers replace the hedges

| Framing | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Far leaked | Hedges left |
|---|---|---|---|---|---|---|---|
| physics | 6/10 | 0.03 (0.00) | 8/10 | 0.12 (0.01) | 9/10 | 1 | 0 |
| neutral | 5/10 | 0.02 (0.00) | 9/10 | 0.05 (0.01) | 8/10 | 0 | 2 |

## Every far episode

| Framing | Readings | Item | Law | T | Measured at | Answer | Data law | Earth | t² fit | Quad fit | Closest | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| physics | exact | FF-F-01 | d = 3 * t^3 | 7 | 1, 2, 3 | 1029 | 1029 | 240.1 | 414 | 669 | data law | 0.0 |
| physics | exact | FF-F-02 | d = 2 * t^3 | 8 | 1, 2, 3 | 1024 | 1024 | 313.6 | 360.4898 | 604 | data law | 0.0 |
| physics | exact | FF-F-03 | d = 12 * t | 9 | 1, 2, 3 | 108 | 108 | 396.9 | 357.0612 | 108 | data law = quadratic fit | 0.0 |
| physics | exact | FF-F-04 | d = 15 * t | 10 | 1, 2, 3 | 150 | 150 | 490 | 551.0204 | 150 | data law = quadratic fit | 0.0 |
| physics | exact | FF-F-05 | d = 1 * t^3 | 11 | 1, 2, 3 | 1331 | 1331 | 592.9 | 340.7755 | 611 | data law | 0.0 |
| physics | exact | FF-F-06 | d = 10 * t | 12 | 1, 2, 3 | 120 | 120 | 705.6 | 528.9796 | 120 | data law = quadratic fit | 0.0 |
| physics | exact | FF-F-07 | d = 20 * t | 13 | 1, 2, 3 | 260 | 260 | 828.1 | 1241.6327 | 260 | data law = quadratic fit | 0.0 |
| physics | exact | FF-F-08 | d = 8 * t | 14 | 1, 2, 3 | 112 | 112 | 960.4 | 576 | 112 | data law = quadratic fit | 0.0 |
| physics | exact | FF-F-09 | d = 0.5 * t^3 | 15 | 1, 2, 3 | 1687.5 | 1687.5 | 1102.5 | 316.8367 | 595.5 | data law | 0.0 |
| physics | exact | FF-F-10 | d = 1.5 * t^3 | 16 | 1, 2, 3 | 6144 | 6144 | 1254.4 | 1081.4694 | 2049 | data law | 0.0 |
| physics | noisy | FF-F-01 | d = 3 * t^3 | 7 | 1, 2, 3, 4, 5, 6 | hedge | 1029 | 240.1 | 740.4089 | 891.31 | hedge |  |
| physics | noisy | FF-F-02 | d = 2 * t^3 | 8 | 1, 2, 3, 4, 5, 6 | 951.296 | 1024 | 313.6 | 646.6174 | 827.6105 | data law | 0.1023 |
| physics | noisy | FF-F-03 | d = 12 * t | 9 | 1, 2, 3, 4, 5, 6 | 114.008 | 108 | 396.9 | 196.4657 | 110.9181 | quadratic fit | 0.0208 |
| physics | noisy | FF-F-04 | d = 15 * t | 10 | 1, 2, 3, 4, 5, 6 | 150 | 150 | 490 | 291.1581 | 156.534 | data law | 0.0 |
| physics | noisy | FF-F-05 | d = 1 * t^3 | 11 | 1, 2, 3 | 572.548 | 1331 | 592.9 | 344.187 | 572.548 | quadratic fit | 1.0276 |
| physics | noisy | FF-F-06 | d = 10 * t | 12 | 1, 2, 3, 4, 5, 6, 1, 2 | 120 | 120 | 705.6 | 276.0976 | 83.4145 | data law | 0.0 |
| physics | noisy | FF-F-07 | d = 20 * t | 13 | 1, 2, 3, 4, 5, 6 | 264.81 | 260 | 828.1 | 661.3796 | 312.8892 | data law | 0.0085 |
| physics | noisy | FF-F-08 | d = 8 * t | 14 | 1, 2, 3, 4, 5, 6, 1, 2 | 115 | 112 | 960.4 | 303.6654 | 57.2246 | data law | 0.0035 |
| physics | noisy | FF-F-09 | d = 0.5 * t^3 | 15 | 1, 2, 3, 4, 5 | 1739.62 | 1687.5 | 1102.5 | 544.8902 | 910.1599 | data law | -0.0891 |
| physics | noisy | FF-F-10 | d = 1.5 * t^3 | 16 | 1, 2, 3, 4, 5, 6 | hedge | 6144 | 1254.4 | 2022.0504 | 2872.2187 | hedge |  |
| neutral | exact | FF-F-01 | d = 3 * t^3 | 7 | 1, 2, 3, 4, 5, 6 | 1029 | 1029 | 240.1 | 788.3723 | 953.4 | data law | 0.0 |
| neutral | exact | FF-F-02 | d = 2 * t^3 | 8 | 1, 2, 3, 4 | 1024 | 1024 | 313.6 | 470.0565 | 713.8 | data law | 0.0 |
| neutral | exact | FF-F-03 | d = 12 * t | 9 | 1, 2, 3 | 108 | 108 | 396.9 | 357.0612 | 108 | data law = quadratic fit | 0.0 |
| neutral | exact | FF-F-04 | d = 15 * t | 10 | 1, 2, 3 | 150 | 150 | 490 | 551.0204 | 150 | data law = quadratic fit | 0.0 |
| neutral | exact | FF-F-05 | d = 1 * t^3 | 11 | 1, 2, 3 | 1331 | 1331 | 592.9 | 340.7755 | 611 | data law | 0.0 |
| neutral | exact | FF-F-06 | d = 10 * t | 12 | 1, 2, 3 | 120 | 120 | 705.6 | 528.9796 | 120 | data law = quadratic fit | 0.0 |
| neutral | exact | FF-F-07 | d = 20 * t | 13 | 1, 2, 3 | 260 | 260 | 828.1 | 1241.6327 | 260 | data law = quadratic fit | 0.0 |
| neutral | exact | FF-F-08 | d = 8 * t | 14 | 1, 2, 3 | 112 | 112 | 960.4 | 576 | 112 | data law = quadratic fit | 0.0 |
| neutral | exact | FF-F-09 | d = 0.5 * t^3 | 15 | 1, 2, 3, 4 | 1687.5 | 1687.5 | 1102.5 | 413.1356 | 723.75 | data law | 0.0 |
| neutral | exact | FF-F-10 | d = 1.5 * t^3 | 16 | 1, 2, 3, 4 | 6144 | 6144 | 1254.4 | 1410.1695 | 2494.95 | data law | 0.0 |
| neutral | noisy | FF-F-01 | d = 3 * t^3 | 7 | 1, 2, 3, 4, 5, 6 | hedge | 1029 | 240.1 | 740.4089 | 891.31 | hedge |  |
| neutral | noisy | FF-F-02 | d = 2 * t^3 | 8 | 1, 2, 3, 4, 5, 6 | hedge | 1024 | 313.6 | 646.6174 | 827.6105 | hedge |  |
| neutral | noisy | FF-F-03 | d = 12 * t | 9 | 1, 2, 3, 4, 5, 6 | 113.76 | 108 | 396.9 | 196.4657 | 110.9181 | quadratic fit | 0.0199 |
| neutral | noisy | FF-F-04 | d = 15 * t | 10 | 1, 2, 3, 4, 5, 6 | 153.633 | 150 | 490 | 291.1581 | 156.534 | data law = quadratic fit | 0.0107 |
| neutral | noisy | FF-F-05 | d = 1 * t^3 | 11 | 1, 2, 3, 4, 5, 6 | hedge | 1331 | 592.9 | 602.549 | 842.073 | hedge |  |
| neutral | noisy | FF-F-06 | d = 10 * t | 12 | 1, 2, 3, 4, 5, 6 | 120 | 120 | 705.6 | 272.3067 | 79.7465 | data law | 0.0 |
| neutral | noisy | FF-F-07 | d = 20 * t | 13 | 1, 2, 3, 4, 5, 6 | 262.189 | 260 | 828.1 | 661.3796 | 312.8892 | data law | 0.0039 |
| neutral | noisy | FF-F-08 | d = 8 * t | 14 | 1, 2, 3, 4, 5, 6 | 110.43 | 112 | 960.4 | 299.5727 | 46.8747 | data law | -0.0019 |
| neutral | noisy | FF-F-09 | d = 0.5 * t^3 | 15 | 1, 2, 3, 4, 5, 6 | hedge | 1687.5 | 1102.5 | 580.6925 | 778.7523 | hedge |  |
| neutral | noisy | FF-F-10 | d = 1.5 * t^3 | 16 | 1, 2, 3, 4, 5, 6 | 5734.4 | 6144 | 1254.4 | 2022.0504 | 2872.2187 | data law | 0.0838 |
