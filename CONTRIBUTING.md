# Contributing

Open an issue describing a reproducible founder problem before adding a role.
Prefer a better existing workflow over more agents. Keep default context small.

1. Make a focused branch and add regression tests for helper changes.
2. Run `python scripts/validate_pack.py` and `python -m unittest discover -s tests -v`.
3. Include the exact environment, commands, and results in your pull request.
4. For visual changes include original before/after previews and crop/overflow
   results. Do not commit copied brand references, private context, or fonts.
5. For workflow changes run appropriate cases in `evals/cases.json` in a real
   host and disclose the model, mode, date, and actual usage when available.

No fabricated benchmarks, guaranteed virality, unsupported security claims,
secret-dependent CI, default telemetry, or mandatory paid model calls.
Sources require dates and access status. An inaccessible video cannot be marked
watched. Review dependencies and license changes explicitly.

Contributions are made under this repository's MIT license. Keep issue threads
respectful and useful; see CODE_OF_CONDUCT.md.
