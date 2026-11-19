# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 30 calls.

Total cost $0.0407.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 3 | 2 | 5 | 0 | 2.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | -0.01 | 0.00 | 5 | 0 | 0 | 2 | 5 | 0 |
| far | 10 | 0.02 | 0.01 | 6 | 0 | 0 | 1 | 4 | 0 |

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-01 | real | 7 | 240.1 | 240.1 | 262.938 | 9.51% | incorrect | n/a |
| FF-R-02 | real | 8 | 313.6 | 313.6 | (no_answer_line) |  | hedge | n/a |
| FF-R-03 | real | 9 | 396.9 | 396.9 | (no_answer_line) |  | hedge | n/a |
| FF-R-04 | real | 10 | 490 | 490 | 500 | 2.04% | correct | n/a |
| FF-R-05 | real | 11 | 592.9 | 592.9 | 511.368 | 13.75% | incorrect | n/a |
| FF-R-06 | real | 12 | 705.6 | 705.6 | (no_answer_line) |  | hedge | n/a |
| FF-R-07 | real | 13 | 828.1 | 828.1 | 845 | 2.04% | correct | n/a |
| FF-R-08 | real | 14 | 960.4 | 960.4 | 980 | 2.04% | correct | n/a |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | (no_answer_line) |  | hedge | n/a |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | (no_answer_line) |  | hedge | n/a |
| FF-N-01 | near_smaller_constant | 7 | 98 | 240.1 | 98 | 0.0 | tracked | n/a |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 162 | 0.013 | tracked | n/a |
| FF-N-03 | near_larger_constant | 9 | 567 | 396.9 | (no_answer_line) |  | hedge | n/a |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | n/a |
| FF-N-05 | near_smaller_constant | 11 | 181.5 | 592.9 | 156.544 | -0.0607 | tracked | n/a |
| FF-N-06 | near_larger_constant | 12 | 1296 | 705.6 | (no_answer_line) |  | hedge | n/a |
| FF-N-07 | near_larger_constant | 13 | 1690 | 828.1 | 1703 | -0.0151 | tracked | n/a |
| FF-N-08 | near_larger_constant | 14 | 2352 | 960.4 | (no_answer_line) |  | hedge | n/a |
| FF-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | (no_answer_line) |  | hedge | n/a |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | (no_answer_line) |  | hedge | n/a |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | (no_answer_line) |  | hedge | n/a |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | (no_answer_line) |  | hedge | n/a |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 113.76 | 0.0199 | tracked | n/a |
| FF-F-04 | far_changed_form | 10 | 150 | 490 | 153.633 | 0.0107 | tracked | n/a |
| FF-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | (no_answer_line) |  | hedge | n/a |
| FF-F-06 | far_changed_form | 12 | 120 | 705.6 | 120 | 0.0 | tracked | n/a |
| FF-F-07 | far_changed_form | 13 | 260 | 828.1 | 262.189 | 0.0039 | tracked | n/a |
| FF-F-08 | far_changed_form | 14 | 112 | 960.4 | 110.43 | -0.0019 | tracked | n/a |
| FF-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | (no_answer_line) |  | hedge | n/a |
| FF-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | 5734.4 | 0.0838 | tracked | n/a |
