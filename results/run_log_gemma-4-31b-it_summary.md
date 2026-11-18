# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 30 calls.

Total cost $0.0049.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 10 | 0 | 0 | 0 | 0.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | 0.00 | 0.00 | 10 | 0 | 0 | 0 | 0 | 0 |
| far | 10 | 0.00 | 0.00 | 10 | 0 | 0 | 0 | 0 | 0 |

Borderline called out (not counted above; see `called_out_coding.csv`): FF-F-09, FF-F-10.

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-01 | real | 7 | 240.1 | 240.1 | 240.1 | 0.0% | correct | no |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | no |
| FF-R-03 | real | 9 | 396.9 | 396.9 | 396.9 | 0.0% | correct | no |
| FF-R-04 | real | 10 | 490 | 490 | 490 | 0.0% | correct | no |
| FF-R-05 | real | 11 | 592.9 | 592.9 | 592.9 | 0.0% | correct | no |
| FF-R-06 | real | 12 | 705.6 | 705.6 | 705.6 | 0.0% | correct | no |
| FF-R-07 | real | 13 | 828.1 | 828.1 | 828.1 | 0.0% | correct | no |
| FF-R-08 | real | 14 | 960.4 | 960.4 | 960.4 | 0.0% | correct | no |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | 1102.5 | 0.0% | correct | no |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | 1254.4 | 0.0% | correct | no |
| FF-N-01 | near_smaller_constant | 7 | 98 | 240.1 | 98 | 0.0 | tracked | no |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | no |
| FF-N-03 | near_larger_constant | 9 | 567 | 396.9 | 567 | 0.0 | tracked | no |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | no |
| FF-N-05 | near_smaller_constant | 11 | 181.5 | 592.9 | 181.5 | 0.0 | tracked | no |
| FF-N-06 | near_larger_constant | 12 | 1296 | 705.6 | 1296 | 0.0 | tracked | no |
| FF-N-07 | near_larger_constant | 13 | 1690 | 828.1 | 1690 | 0.0 | tracked | no |
| FF-N-08 | near_larger_constant | 14 | 2352 | 960.4 | 2352 | 0.0 | tracked | no |
| FF-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | 675 | 0.0 | tracked | no |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | 307.2 | 0.0 | tracked | no |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | 1029 | 0.0 | tracked | no |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | no |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | no |
| FF-F-04 | far_changed_form | 10 | 150 | 490 | 150 | 0.0 | tracked | no |
| FF-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | 1331 | 0.0 | tracked | no |
| FF-F-06 | far_changed_form | 12 | 120 | 705.6 | 120 | 0.0 | tracked | no |
| FF-F-07 | far_changed_form | 13 | 260 | 828.1 | 260 | 0.0 | tracked | no |
| FF-F-08 | far_changed_form | 14 | 112 | 960.4 | 112 | 0.0 | tracked | no |
| FF-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | 1687.5 | 0.0 | tracked | borderline |
| FF-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | 6144 | 0.0 | tracked | borderline |
