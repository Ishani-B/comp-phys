# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature default, seed none, reasoning off, 50 calls.

Total cost $0.0081.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 10 | 0 | 0 | 0 | 0.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 20 | 0.00 | 0.00 | 20 | 0 | 0 | 0 | 0 | 0 |
| far | 20 | 0.00 | 0.00 | 20 | 0 | 0 | 0 | 0 | 0 |

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-R-02 | real | 8 | 313.6 | 313.6 | 313.6 | 0.0% | correct | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-02 | near_smaller_constant | 8 | 160 | 313.6 | 160 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-N-04 | near_larger_constant | 10 | 800 | 490 | 800 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-02 | far_changed_exponent | 8 | 1024 | 313.6 | 1024 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
| FF-F-03 | far_changed_form | 9 | 108 | 396.9 | 108 | 0.0 | tracked | not coded |
