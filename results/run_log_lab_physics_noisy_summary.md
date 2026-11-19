# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 30 calls.

Total cost $0.0402.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 4 | 4 | 2 | 0 | 6.1 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | -0.00 | -0.00 | 8 | 1 | 0 | 5 | 1 | 0 |
| far | 10 | 0.13 | 0.01 | 7 | 0 | 1 | 2 | 2 | 5 |

Borderline called out (not counted above; see `called_out_coding.csv`): FF-F-01, FF-F-02, FF-F-09.

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-01 | real | 7 | 240.1 | 240.1 | 312.571 | 30.18% | incorrect | no |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 288 | 8.16% | incorrect | no |
| FF-R-03 | real | 9 | 396.9 | 396.9 | (no_answer_line) |  | hedge | no |
| FF-R-04 | real | 10 | 490 | 490 | 475 | 3.06% | correct | no |
| FF-R-05 | real | 11 | 592.9 | 592.9 | 592.9 | 0.0% | correct | no |
| FF-R-06 | real | 12 | 705.6 | 705.6 | 913.377 | 29.45% | incorrect | no |
| FF-R-07 | real | 13 | 828.1 | 828.1 | (no_answer_line) |  | hedge | no |
| FF-R-08 | real | 14 | 960.4 | 960.4 | 921.2 | 4.08% | correct | no |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | 1117.01 | 1.32% | correct | no |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | 1356.256 | 8.12% | incorrect | no |
| FF-N-01 | near_smaller_constant | 7 | 98 | 240.1 | 94.57 | -0.0241 | tracked | no |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 151.04 | -0.0583 | tracked | no |
| FF-N-03 | near_larger_constant | 9 | 567 | 396.9 | 589.28 | -0.131 | tracked | no |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 786.4 | 0.0439 | tracked | no |
| FF-N-05 | near_smaller_constant | 11 | 181.5 | 592.9 | 179.84 | -0.004 | tracked | no |
| FF-N-06 | near_larger_constant | 12 | 1296 | 705.6 | 1677.621 | -0.6464 | tracked | no |
| FF-N-07 | near_larger_constant | 13 | 1690 | 828.1 | 1070.077 | 0.7193 | between | no |
| FF-N-08 | near_larger_constant | 14 | 2352 | 960.4 | 2257.724 | 0.0677 | tracked | no |
| FF-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | 675 | 0.0 | tracked | no |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | (no_answer_line) |  | hedge | no |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | (no_answer_line) |  | hedge | borderline |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 951.296 | 0.1023 | tracked | borderline |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 114.008 | 0.0208 | tracked | yes |
| FF-F-04 | far_changed_form | 10 | 150 | 490 | 150 | 0.0 | tracked | yes |
| FF-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | 572.548 | 1.0276 | leaked | no |
| FF-F-06 | far_changed_form | 12 | 120 | 705.6 | 120 | 0.0 | tracked | yes |
| FF-F-07 | far_changed_form | 13 | 260 | 828.1 | 264.81 | 0.0085 | tracked | yes |
| FF-F-08 | far_changed_form | 14 | 112 | 960.4 | 115 | 0.0035 | tracked | yes |
| FF-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | 1739.625 | -0.0891 | tracked | borderline |
| FF-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | (no_answer_line) |  | hedge | no |
