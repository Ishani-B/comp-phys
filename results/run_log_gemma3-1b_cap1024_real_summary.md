# Summary: gemma3:1b

Model digest `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`, 999.89M, Q4_K_M, Ollama 0.40.16, temperature 0.0, 10 calls.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 1 | 2 | 7 | 0 | 76.9 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-01 | real | 7 | 240.1 | 240.1 | (no_answer_line) |  | hedge | no |
| FF-R-02 | real | 8 | 313.6 | 313.6 | (no_answer_line) |  | hedge | no |
| FF-R-03 | real | 9 | 396.9 | 396.9 | (no_answer_line) |  | hedge | no |
| FF-R-04 | real | 10 | 490 | 490 | 490 | 0.0% | correct | no |
| FF-R-05 | real | 11 | 592.9 | 592.9 | (no_answer_line) |  | hedge | no |
| FF-R-06 | real | 12 | 705.6 | 705.6 | (no_answer_line) |  | hedge | no |
| FF-R-07 | real | 13 | 828.1 | 828.1 | 191.1 | 76.92% | incorrect | no |
| FF-R-08 | real | 14 | 960.4 | 960.4 | 205.8 | 78.57% | incorrect | no |
| FF-R-09 | real | 15 | 1102.5 | 1102.5 | (no_answer_line) |  | hedge | no |
| FF-R-10 | real | 16 | 1254.4 | 1254.4 | (no_answer_line) |  | hedge | no |
