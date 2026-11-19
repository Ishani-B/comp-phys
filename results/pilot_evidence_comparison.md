# Gemma 4 31B across evidence levels

Normalized score: 0 = followed the data's law, 1 = gave the real-world answer. Real-law items show the number correct within 5%.

| Evidence | Real-law control | Near: mean (median) | Near tracked | Far: mean (median) | Far tracked | Hedges | Called out |
|---|---|---|---|---|---|---|---|
| exact, 6 points (Starter) | 10/10 | 0.00 (0.00) | 10/10 | 0.00 (0.00) | 10/10 | 0 | 0 |
| noisy, 6 points | 9/10 | 0.03 (0.03) | 10/10 | 0.19 (0.00) | 8/10 | 1 | 1 |
| exact, 3 points | 10/10 | 0.00 (0.00) | 10/10 | 0.00 (0.00) | 10/10 | 0 | 0 |

## Far items: which reference each answer is closest to

| Evidence | Item | Law in data | T | Answer | Data law | Real law | t² fit | Quadratic fit | Closest |
|---|---|---|---|---|---|---|---|---|---|
| exact, 6 points (Starter) | FF-F-01 | d = 3 * t^3 | 7 | 1029 | 1029 | 240.1 | 788.4 | 953.4 | data law |
| exact, 6 points (Starter) | FF-F-02 | d = 2 * t^3 | 8 | 1024 | 1024 | 313.6 | 686.5 | 887.2 | data law |
| exact, 6 points (Starter) | FF-F-03 | d = 12 * t | 9 | 108 | 108 | 396.9 | 188.4 | 108.0 | data law = quadratic fit |
| exact, 6 points (Starter) | FF-F-04 | d = 15 * t | 10 | 150 | 150 | 490 | 290.8 | 150.0 | data law = quadratic fit |
| exact, 6 points (Starter) | FF-F-05 | d = 1 * t^3 | 11 | 1331 | 1331 | 592.9 | 648.9 | 947.0 | data law |
| exact, 6 points (Starter) | FF-F-06 | d = 10 * t | 12 | 120 | 120 | 705.6 | 279.1 | 120.0 | data law = quadratic fit |
| exact, 6 points (Starter) | FF-F-07 | d = 20 * t | 13 | 260 | 260 | 828.1 | 655.2 | 260.0 | data law = quadratic fit |
| exact, 6 points (Starter) | FF-F-08 | d = 8 * t | 14 | 112 | 112 | 960.4 | 304.0 | 112.0 | data law = quadratic fit |
| exact, 6 points (Starter) | FF-F-09 | d = 0.5 * t^3 | 15 | 1687.5 | 1687.5 | 1102.5 | 603.3 | 956.1 | data law |
| exact, 6 points (Starter) | FF-F-10 | d = 1.5 * t^3 | 16 | 6144 | 6144 | 1254.4 | 2059.4 | 3309.0 | data law |
| noisy, 6 points | FFNZ-F-02 | d = 2 * t^3 | 8 | 1024 | 1024 | 313.6 | 713.1 | 981.3 | data law |
| noisy, 6 points | FFNZ-F-03 | d = 12 * t | 9 | 142.1 | 108 | 396.9 | 197.4 | 128.1 | quadratic fit |
| noisy, 6 points | FFNZ-F-04 | d = 15 * t | 10 | 136.5 | 150 | 490 | 273.3 | 122.0 | data law |
| noisy, 6 points | FFNZ-F-05 | d = 1 * t^3 | 11 | 1331 | 1331 | 592.9 | 635.8 | 847.3 | data law |
| noisy, 6 points | FFNZ-F-06 | d = 10 * t | 12 | 115 | 120 | 705.6 | 274.0 | 109.6 | data law = quadratic fit |
| noisy, 6 points | FFNZ-F-07 | d = 20 * t | 13 | 249.5 | 260 | 828.1 | 639.3 | 203.9 | data law |
| noisy, 6 points | FFNZ-F-08 | d = 8 * t | 14 | 113.4 | 112 | 960.4 | 298.6 | 128.5 | data law |
| noisy, 6 points | FFNZ-F-09 | d = 0.5 * t^3 | 15 | 612.3 | 1687.5 | 1102.5 | 574.0 | 813.5 | t² fit |
| noisy, 6 points | FFNZ-F-10 | d = 1.5 * t^3 | 16 | 7057.6 | 6144 | 1254.4 | 2157.1 | 3785.5 | data law |
| exact, 3 points | FFSP-F-01 | d = 3 * t^3 | 7 | 1029 | 1029 | 240.1 | 414.0 | 669.0 | data law |
| exact, 3 points | FFSP-F-02 | d = 2 * t^3 | 8 | 1024 | 1024 | 313.6 | 360.5 | 604.0 | data law |
| exact, 3 points | FFSP-F-03 | d = 12 * t | 9 | 108 | 108 | 396.9 | 357.1 | 108.0 | data law = quadratic fit |
| exact, 3 points | FFSP-F-04 | d = 15 * t | 10 | 150 | 150 | 490 | 551.0 | 150.0 | data law = quadratic fit |
| exact, 3 points | FFSP-F-05 | d = 1 * t^3 | 11 | 1331 | 1331 | 592.9 | 340.8 | 611.0 | data law |
| exact, 3 points | FFSP-F-06 | d = 10 * t | 12 | 120 | 120 | 705.6 | 529.0 | 120.0 | data law = quadratic fit |
| exact, 3 points | FFSP-F-07 | d = 20 * t | 13 | 260 | 260 | 828.1 | 1241.6 | 260.0 | data law = quadratic fit |
| exact, 3 points | FFSP-F-08 | d = 8 * t | 14 | 112 | 112 | 960.4 | 576.0 | 112.0 | data law = quadratic fit |
| exact, 3 points | FFSP-F-09 | d = 0.5 * t^3 | 15 | 1687.5 | 1687.5 | 1102.5 | 316.8 | 595.5 | data law |
| exact, 3 points | FFSP-F-10 | d = 1.5 * t^3 | 16 | 6144 | 6144 | 1254.4 | 1081.5 | 2049.0 | data law |
