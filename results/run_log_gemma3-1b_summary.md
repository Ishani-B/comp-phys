# Summary: gemma3:1b

Model digest `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`, 999.89M, Q4_K_M, Ollama 0.40.16, temperature 0.0, 30 calls.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 4 | 6 | 0 | 0 | 63.4 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | -7104.82 | -0.11 | 6 | 1 | 2 | 7 | 1 | 0 |
| far | 10 | 0.57 | 0.30 | 5 | 1 | 4 | 3 | 0 | 0 |

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-01 | real | 7 | 240.1 | 240.1 | 240.1 | 0.0% | correct | no |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | no |
| FF-R-03 | real | 9 | 396.9 | 396.9 | 186.2 | 53.09% | incorrect | no |
| FF-R-04 | real | 10 | 490 | 490 | 490 | 0.0% | correct | no |
| FF-R-05 | real | 11 | 592.9 | 592.9 | 592.9 | 0.0% | correct | no |
| FF-R-06 | real | 12 | 705.6 | 705.6 | 186.2 | 73.61% | incorrect | no |
| FF-R-07 | real | 13 | 828.1 | 828.1 | 191.1 | 76.92% | incorrect | no |
| FF-R-08 | real | 14 | 960.4 | 960.4 | 205.8 | 78.57% | incorrect | no |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | 73.5 | 93.33% | incorrect | no |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | 186.2 | 85.16% | incorrect | no |
| FF-N-01 | near_smaller_constant | 7 | 98 | 240.1 | 147 | 0.3448 | between | no |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 142.5 | -0.1139 | tracked | no |
| FF-N-03 | near_larger_constant | 9 | 567 | 396.9 | 119 | 2.6337 | leaked | no |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 4096 | -10.6323 | tracked | no |
| FF-N-05 | near_smaller_constant | 11 | 181.5 | 592.9 | 181.5 | 0.0 | tracked | no |
| FF-N-06 | near_larger_constant | 12 | 1296 | 705.6 | 37748736 | -63935.3659 | tracked | no |
| FF-N-07 | near_larger_constant | 13 | 1690 | 828.1 | (no_answer_line) |  | hedge | no |
| FF-N-08 | near_larger_constant | 14 | 2352 | 960.4 | 576 | 1.2762 | leaked | no |
| FF-N-09 | near_smaller_constant | 15 | 675 | 1102.5 | 147 | -1.2351 | tracked | no |
| FF-N-10 | near_smaller_constant | 16 | 307.2 | 1254.4 | 55.2 | -0.266 | tracked | no |
| FF-F-01 | far_changed_exponent | 7 | 1029 | 240.1 | 129 | 1.1408 | leaked | no |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 604 | 0.5912 | between | no |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | no |
| FF-F-04 | far_changed_form | 10 | 150 | 490 | 150 | 0.0 | tracked | no |
| FF-F-05 | far_changed_exponent | 11 | 1331 | 592.9 | 611 | 0.9755 | leaked | no |
| FF-F-06 | far_changed_form | 12 | 120 | 705.6 | 120 | 0.0 | tracked | no |
| FF-F-07 | far_changed_form | 13 | 260 | 828.1 | 260 | 0.0 | tracked | no |
| FF-F-08 | far_changed_form | 14 | 112 | 960.4 | 112 | 0.0 | tracked | no |
| FF-F-09 | far_changed_exponent | 15 | 1687.5 | 1102.5 | 680 | 1.7222 | leaked | no |
| FF-F-10 | far_changed_exponent | 16 | 6144 | 1254.4 | 159 | 1.224 | leaked | no |
