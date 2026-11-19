# Consistency check: Gemma 4 31B at the default temperature

Design: "Consistency check" in `PLAN.md`. 10 samples per item, temperature and seed left to the provider's defaults, everything else as in the Starter.

| Item | Law | Correct (data) | Temp-0 answer | Default-temp answers (10) | Min | Max | SD | Distinct replies | Same label as temp 0 | Labels |
|---|---|---|---|---|---|---|---|---|---|---|
| FF-R-02 | d = 4.9 * t^2 | 313.6 | 313.6 | 313.6, 313.6, 313.6, 313.6, 313.6, 313.6, 313.6, 313.6, 313.6, 313.6 | 313.6 | 313.6 | 0 | 10/10 | 10/10 | correct 10 |
| FF-N-02 | d = 2.5 * t^2 | 160 | 160 | 160, 160, 160, 160, 160, 160, 160, 160, 160, 160 | 160 | 160 | 0 | 10/10 | 10/10 | tracked 10 |
| FF-N-04 | d = 8 * t^2 | 800 | 800 | 800, 800, 800, 800, 800, 800, 800, 800, 800, 800 | 800 | 800 | 0 | 10/10 | 10/10 | tracked 10 |
| FF-F-02 | d = 2 * t^3 | 1024 | 1024 | 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024 | 1024 | 1024 | 0 | 10/10 | 10/10 | tracked 10 |
| FF-F-03 | d = 12 * t | 108 | 108 | 108, 108, 108, 108, 108, 108, 108, 108, 108, 108 | 108 | 108 | 0 | 10/10 | 10/10 | tracked 10 |

**Overall:** 50 of 50 default-temperature answers keep the temperature-0 label; 0 hedges. Cost $0.0081.

The provider really sampled: every reply's wording differs ("Distinct replies"), and lengths vary. So the identical answers come from the model, not from a deterministic default.

