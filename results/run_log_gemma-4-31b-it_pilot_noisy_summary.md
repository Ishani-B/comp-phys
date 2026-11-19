# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 30 calls.

Total cost $0.0133.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 9 | 1 | 0 | 0 | 2.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | 0.03 | 0.03 | 10 | 0 | 0 | 2 | 0 | 0 |
| far | 10 | 0.19 | 0.00 | 8 | 0 | 1 | 5 | 1 | 1 |

Borderline called out (not counted above; see `called_out_coding.csv`): FFNZ-F-01, FFNZ-F-02, FFNZ-F-03, FFNZ-F-04, FFNZ-F-06, FFNZ-F-07, FFNZ-F-08, FFNZ-F-09, FFNZ-F-10.

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FFNZ-R-01 | real | 7 | 240.1 | 240.1 | 255.8 | 6.54% | incorrect | no |
| FFNZ-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | no |
| FFNZ-R-03 | real | 9 | 396.9 | 396.9 | 405 | 2.04% | correct | no |
| FFNZ-R-04 | real | 10 | 490 | 490 | 465.5 | 5.0% | correct | no |
| FFNZ-R-05 | real | 11 | 592.9 | 592.9 | 605 | 2.04% | correct | no |
| FFNZ-R-06 | real | 12 | 705.6 | 705.6 | 691.2 | 2.04% | correct | no |
| FFNZ-R-07 | real | 13 | 828.1 | 828.1 | 828.1 | 0.0% | correct | no |
| FFNZ-R-08 | real | 14 | 960.4 | 960.4 | 980 | 2.04% | correct | no |
| FFNZ-R-09 | real | 15 | 1102.5 | 1102.5 | 1125 | 2.04% | correct | no |
| FFNZ-R-10 | real | 16 | 1254.4 | 1254.4 | 1280 | 2.04% | correct | no |
| FFNZ-N-01 | near_smaller_constant | 7 | 98 | 240.1 | 105.3 | 0.0514 | tracked | no |
| FFNZ-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 158.4 | -0.0104 | tracked | no |
| FFNZ-N-03 | near_larger_constant | 9 | 567 | 396.9 | 558.9 | 0.0476 | tracked | no |
| FFNZ-N-04 | near_larger_constant | 10 | 800 | 490 | 760 | 0.129 | tracked | no |
| FFNZ-N-05 | near_smaller_constant | 11 | 181.5 | 592.9 | 184.4 | 0.007 | tracked | no |
| FFNZ-N-06 | near_larger_constant | 12 | 1296 | 705.6 | 1243.2 | 0.0894 | tracked | no |
| FFNZ-N-07 | near_larger_constant | 13 | 1690 | 828.1 | 1658.4 | 0.0367 | tracked | no |
| FFNZ-N-08 | near_larger_constant | 14 | 2352 | 960.4 | 2450 | -0.0704 | tracked | no |
| FFNZ-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | 683.3 | 0.0194 | tracked | no |
| FFNZ-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | 312.32 | 0.0054 | tracked | no |
| FFNZ-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | (no_answer_line) |  | hedge | borderline |
| FFNZ-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | borderline |
| FFNZ-F-03 | far_changed_form | 9 | 108 | 396.9 | 142.1 | 0.118 | tracked | borderline |
| FFNZ-F-04 | far_changed_form | 10 | 150 | 490 | 136.5 | -0.0397 | tracked | borderline |
| FFNZ-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | 1331 | 0.0 | tracked | yes |
| FFNZ-F-06 | far_changed_form | 12 | 120 | 705.6 | 115 | -0.0085 | tracked | borderline |
| FFNZ-F-07 | far_changed_form | 13 | 260 | 828.1 | 249.5 | -0.0185 | tracked | borderline |
| FFNZ-F-08 | far_changed_form | 14 | 112 | 960.4 | 113.4 | 0.0017 | tracked | borderline |
| FFNZ-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | 612.3 | 1.8379 | leaked | borderline |
| FFNZ-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | 7057.6 | -0.1868 | tracked | borderline |
