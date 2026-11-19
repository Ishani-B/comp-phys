# Summary: google/gemma-4-31b-it

OpenRouter, provider Crusoe (bf16), served as `google/gemma-4-31b-it`, temperature 0.0, seed 0, reasoning off, 30 calls.

Total cost $0.0116.

## Real-law control (can the model do the task at all?)

| Items | Correct (within 5%) | Incorrect | Hedge | Called out | Median % error |
|---|---|---|---|---|---|
| 10 | 10 | 0 | 0 | 0 | 0.0 |

## Counterfactual conditions

Normalized score: 0 = followed the data, 1 = gave the real-world answer.

| Law distance | Items | Mean score | Median score | Tracked (<=0.2) | Between | Leaked (>=0.8) | Outside 0-1 | Hedge | Called out |
|---|---|---|---|---|---|---|---|---|---|
| near | 10 | -0.05 | -0.00 | 10 | 0 | 0 | 5 | 0 | 7 |
| far | 10 | 0.00 | 0.00 | 10 | 0 | 0 | 0 | 0 | 1 |

Borderline called out (not counted above; see `called_out_coding.csv`): KP-N-02, KP-N-05, KP-N-08, KP-F-01, KP-F-05.

The mean is the locked outcome. The median is shown as well because a single wild answer can move the mean a long way with 10 items.

## Every call

| Item | Variant | T | Correct (data) | Real-world | Model answer | Score / % error | Label | Called out |
|---|---|---|---|---|---|---|---|---|
| KP-R-01 | real | 7 | 22.2243 | 22.2288 | 22.22 | 0.04% | correct | no |
| KP-R-02 | real | 8 | 33.9411 | 33.9428 | 33.94 | 0.01% | correct | no |
| KP-R-03 | real | 9 | 54 | 53.9959 | 54 | 0.01% | correct | no |
| KP-R-04 | real | 10 | 79.0569 | 79.0534 | 79.06 | 0.01% | correct | no |
| KP-R-05 | real | 11 | 109.4486 | 109.4485 | 109.45 | 0.0% | correct | no |
| KP-R-06 | real | 12 | 145.4923 | 145.4938 | 145.5 | 0.0% | correct | no |
| KP-R-07 | real | 13 | 187.4887 | 187.4869 | 187.49 | 0.0% | correct | no |
| KP-R-08 | real | 14 | 261.916 | 261.9044 | 261.9 | 0.0% | correct | no |
| KP-R-09 | real | 15 | 348.5685 | 348.5642 | 348.57 | 0.0% | correct | no |
| KP-R-10 | real | 16 | 512 | 512.0068 | 512 | 0.0% | correct | no |
| KP-N-01 | near_smaller_exponent | 7 | 12.3965 | 13.7275 | 12.4 | 0.0026 | tracked | yes |
| KP-N-02 | near_smaller_exponent | 8 | 18.1886 | 20.9743 | 18.24 | 0.0185 | tracked | borderline |
| KP-N-03 | near_larger_exponent | 9 | 104.3918 | 87.8875 | 103.6 | 0.048 | tracked | yes |
| KP-N-04 | near_larger_exponent | 10 | 157.7393 | 128.6579 | 160.81 | -0.1056 | tracked | yes |
| KP-N-05 | near_smaller_exponent | 11 | 53.308 | 67.6218 | 56 | 0.1881 | tracked | borderline |
| KP-N-06 | near_larger_exponent | 12 | 306.6156 | 236.7873 | 306.6 | 0.0002 | tracked | yes |
| KP-N-07 | near_larger_exponent | 13 | 404.7231 | 305.1338 | 433.6 | -0.29 | tracked | yes |
| KP-N-08 | near_larger_exponent | 14 | 578.0967 | 426.268 | 624.84 | -0.3079 | tracked | borderline |
| KP-N-09 | near_smaller_exponent | 15 | 154.6895 | 215.3362 | 154.3 | -0.0064 | tracked | yes |
| KP-N-10 | near_smaller_exponent | 16 | 222.8609 | 316.3265 | 222.3 | -0.006 | tracked | yes |
| KP-F-01 | far_cubic | 7 | 411.6 | 264.4746 | 411.6 | 0.0 | tracked | borderline |
| KP-F-02 | far_cubic | 8 | 768 | 403.9075 | 768 | 0.0 | tracked | no |
| KP-F-03 | far_linear | 9 | 18 | 24.2851 | 18 | 0.0 | tracked | no |
| KP-F-04 | far_linear | 10 | 25 | 35.5539 | 25 | 0.0 | tracked | no |
| KP-F-05 | far_cubic | 11 | 3993 | 1302.4645 | 3993 | 0.0 | tracked | borderline |
| KP-F-06 | far_linear | 12 | 42 | 65.4315 | 42 | 0.0 | tracked | no |
| KP-F-07 | far_linear | 13 | 52 | 84.3183 | 52 | 0.0 | tracked | no |
| KP-F-08 | far_linear | 14 | 70 | 117.7901 | 70 | 0.0 | tracked | no |
| KP-F-09 | far_cubic | 15 | 20250 | 4148.0479 | 20250 | 0.0 | tracked | yes |
| KP-F-10 | far_cubic | 16 | 32768 | 6092.9216 | 32768 | 0.0 | tracked | no |
