# Summary: anthropic/claude-sonnet-4.6

OpenRouter, provider Anthropic (n/a), served as `anthropic/claude-sonnet-4.6`, temperature 0.0, seed none, reasoning off, 30 calls.

Total cost $0.8719.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 10 | 0 | 0 | 0 | 0.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | -0.22 | 0.00 | 8 | 0 | 0 | 4 | 2 | 0 |
| far | 10 | -0.02 | 0.00 | 10 | 0 | 0 | 1 | 0 | 0 |

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| HK-R-01 | real | 7 | 8.4 | 8.4 | 8.4 | 0.0% | correct | n/a |
| HK-R-02 | real | 8 | 12 | 12 | 12 | 0.0% | correct | n/a |
| HK-R-03 | real | 9 | 18 | 18 | 18 | 0.0% | correct | n/a |
| HK-R-04 | real | 10 | 25 | 25 | 25 | 0.0% | correct | n/a |
| HK-R-05 | real | 11 | 33 | 33 | 33 | 0.0% | correct | n/a |
| HK-R-06 | real | 12 | 42 | 42 | 42 | 0.0% | correct | n/a |
| HK-R-07 | real | 13 | 52 | 52 | 52 | 0.0% | correct | n/a |
| HK-R-08 | real | 14 | 70 | 70 | 70 | 0.0% | correct | n/a |
| HK-R-09 | real | 15 | 90 | 90 | 90 | 0.0% | correct | n/a |
| HK-R-10 | real | 16 | 128 | 128 | 128 | 0.0% | correct | n/a |
| HK-N-01 | near_smaller_exponent | 7 | 4.6854 | 5.3315 | (no_answer_line) |  | hedge | n/a |
| HK-N-02 | near_smaller_exponent | 8 | 6.4306 | 7.6176 | (no_answer_line) |  | hedge | n/a |
| HK-N-03 | near_larger_exponent | 9 | 43.348 | 33.5107 | 43.37 | -0.0022 | tracked | n/a |
| HK-N-04 | near_larger_exponent | 10 | 62.7972 | 46.5473 | 88.8 | -1.6002 | tracked | n/a |
| HK-N-05 | near_smaller_exponent | 11 | 16.073 | 20.9423 | 16.1 | 0.0055 | tracked | n/a |
| HK-N-06 | near_larger_exponent | 12 | 113.4806 | 78.1873 | 113.4 | 0.0023 | tracked | n/a |
| HK-N-07 | near_larger_exponent | 13 | 145.071 | 96.8014 | 151.55 | -0.1342 | tracked | n/a |
| HK-N-08 | near_larger_exponent | 14 | 201.1635 | 130.3154 | 201 | 0.0023 | tracked | n/a |
| HK-N-09 | near_smaller_exponent | 15 | 39.9407 | 57.0989 | 40 | 0.0035 | tracked | n/a |
| HK-N-10 | near_smaller_exponent | 16 | 55.7152 | 81.2062 | 55.7 | -0.0006 | tracked | n/a |
| HK-F-01 | far_quadratic | 7 | 58.8 | 40.7077 | 58.8 | 0.0 | tracked | n/a |
| HK-F-02 | far_quadratic | 8 | 96 | 58.1538 | 96 | 0.0 | tracked | n/a |
| HK-F-03 | far_square_root | 9 | 6 | 8.4847 | 6 | 0.0 | tracked | n/a |
| HK-F-04 | far_square_root | 10 | 7.9057 | 11.7846 | 7.906 | 0.0001 | tracked | n/a |
| HK-F-05 | far_quadratic | 11 | 363 | 159.9231 | 363 | 0.0 | tracked | n/a |
| HK-F-06 | far_square_root | 12 | 12.1244 | 19.8 | 10.78 | -0.1752 | tracked | n/a |
| HK-F-07 | far_square_root | 13 | 14.4222 | 24.5157 | 14.422 | 0.0 | tracked | n/a |
| HK-F-08 | far_square_root | 14 | 18.7083 | 33.0031 | 18.708 | 0.0 | tracked | n/a |
| HK-F-09 | far_quadratic | 15 | 1350 | 436.1538 | 1350 | 0.0 | tracked | n/a |
| HK-F-10 | far_quadratic | 16 | 2048 | 620.3077 | 2048 | 0.0 | tracked | n/a |
