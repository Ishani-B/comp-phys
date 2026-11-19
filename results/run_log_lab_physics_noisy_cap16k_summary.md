# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 5 calls.

Total cost $0.0176.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 2 | 2 | 0 | 0 | 0 | 2.9 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 1 | 0.29 | 0.29 | 0 | 1 | 0 | 0 | 0 | 0 |
| far | 2 | 0.06 | 0.06 | 2 | 0 | 0 | 0 | 0 | 0 |

Borderline called out (not counted above; see `called_out_coding.csv`): FF-F-01.

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-03 | real | 9 | 396.9 | 396.9 | 411.48 | 3.67% | correct | no |
| FF-R-07 | real | 13 | 828.1 | 828.1 | 845 | 2.04% | correct | no |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | 583.68 | 0.2919 | between | no |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | 994.1 | 0.0442 | tracked | borderline |
| FF-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | 5734.4 | 0.0838 | tracked | no |
