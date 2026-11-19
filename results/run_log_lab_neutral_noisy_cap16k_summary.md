# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 14 calls.

Total cost $0.0483.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 5 | 2 | 3 | 0 | 0 | 8.2 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 5 | 0.05 | 0.04 | 4 | 0 | 0 | 1 | 1 | 0 |
| far | 4 | 0.12 | 0.11 | 2 | 1 | 0 | 0 | 1 | 0 |

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-02 | real | 8 | 313.6 | 313.6 | 288 | 8.16% | incorrect | n/a |
| FF-R-03 | real | 9 | 396.9 | 396.9 | 412.5 | 3.93% | correct | n/a |
| FF-R-06 | real | 12 | 705.6 | 705.6 | 720 | 2.04% | correct | n/a |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | 336.457 | 69.48% | incorrect | n/a |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | 886.4 | 29.34% | incorrect | n/a |
| FF-N-03 | near_larger_constant | 9 | 567 | 396.9 | (no_answer_line) |  | hedge | n/a |
| FF-N-06 | near_larger_constant | 12 | 1296 | 705.6 | 1200 | 0.1626 | tracked | n/a |
| FF-N-08 | near_larger_constant | 14 | 2352 | 960.4 | 2254 | 0.0704 | tracked | n/a |
| FF-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | 675 | 0.0 | tracked | n/a |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | 281.6 | -0.027 | tracked | n/a |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | (no_answer_line) |  | hedge | n/a |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 947.2 | 0.1081 | tracked | n/a |
| FF-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | 1331 | 0.0 | tracked | n/a |
| FF-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | 1541.25 | 0.25 | between | n/a |
