# Helper commands

Run from the downloaded repository, or replace `skills/co-founder` with the
absolute installed core path. `PROJECT` is the actual product repository.

```sh
python skills/co-founder/scripts/cf.py init --project PROJECT
python skills/co-founder/scripts/cf.py doctor --project PROJECT
python skills/co-founder/scripts/cf.py context --project PROJECT --task ui-polish --max-bytes 12000
python skills/co-founder/scripts/cf.py impact --project PROJECT --base HEAD
python skills/co-founder/scripts/cf.py impact --project PROJECT --base BASE_COMMIT --map PROJECT/.co-founder/product-map.json
```

The product map has `modules: [{id, paths: [glob]}]` and
`relationships: [{from, to, kind, reason}]`. Impact uses changed/untracked paths and
conservative bidirectional relationship expansion. Unmapped and truncated paths
remain explicit. No imports, database or event semantics are automatically inferred.

## Record an approved local check

```sh
python skills/co-founder/scripts/cf.py run-check --project PROJECT --name unit --timeout 120 -- python -m unittest discover -s tests
python skills/co-founder/scripts/cf.py run-check --project PROJECT --name unit --execute --timeout 120 -- python -m unittest discover -s tests
```

First command is a dry run. Use your project's actual reviewed test command, not
blindly this example. Evidence is placed under the private context directory with
command, return code, duration, Git state, log hashes and limitations. Return code:
0 passed/dry-run; 1 failed or inconclusive execution; 2 invalid input/tool error.
Logs may contain sensitive data. Never pass secrets in command arguments.

## Structural review gate

Copy `assets/templates/verification.json` into your private evidence folder and
populate only actual results. Required checks need passed status, the same candidate
revision, and nonempty evidence references. Review all changes to acceptance rules.

```sh
python skills/co-founder/scripts/cf.py gate --report PROJECT/.co-founder/evidence/review.json
```

Return 0 means ready-for-review, not release approval. Return 1 means blocked or
inconclusive; return 2 means invalid report. Empty required-check lists are invalid.
The gate does not authenticate the referenced artifacts or approvals. Working-tree
changes need additional precise evidence; a HEAD hash plus dirty flag is not a
complete identity for an uncommitted code state.

## On-demand brief and measured usage

```sh
python skills/co-founder/scripts/cf.py brief --project PROJECT --date 2026-09-23 --limit 3
python skills/co-founder/scripts/cf.py metrics --project PROJECT --date 2026-09-23 --stale-days 35
python skills/co-founder/scripts/cf.py usage-summary --project PROJECT
```

Use the actual local date. State entries use id/title/status/priority/due_date/source/
next_action. The brief also ranks open, at-risk and missed items from
`commitments.json`; a missed or due promise defaults to high priority. The local
sort is an aid, not a substitute for the founder's judgment.

`metrics` validates `metrics.json` and reports each metric's latest and previous
snapshot, change, trend against its declared direction, and staleness. It reads
only recorded snapshots; it does not query a bank, payment or analytics account.
Usage-entry syntax and subset accounting are in [TOKEN_DISCIPLINE.md](TOKEN_DISCIPLINE.md).

## Browser evidence

```sh
python skills/co-founder/scripts/ui_audit.py --base http://127.0.0.1:3000 --paths / /settings --out PROJECT/.co-founder/evidence/ui-review --sizes 390x844 768x1024 1440x1000
```

Use an existing approved development server; this helper does not start one.
Output folder must be new. The default blocks resources outside the target origin.
Add an exact `--allow-origin` only after review. `--allow-remote` is required for a
remote target. No login/session credentials are loaded. Static observations cover
horizontal overflow, broken images and an elementary button-label heuristic. They
are not full accessibility, responsive, functional, visual or security verification.
Actual screenshots still require inspection. See [MEDIA.md](MEDIA.md) for browser setup.

### Offline HTML capture

```sh
python skills/co-founder/scripts/ui_audit.py --html reviewed-local-page.html --out NEW_EVIDENCE_FOLDER
```

This renders the reviewed HTML inline and blocks resource requests. It is useful
for self-contained fixtures, not proof of a live site, navigation, authentication
or persistence. Relative assets may not render. Do not execute untrusted HTML.

## New project/craft helpers (1.1)

`project_context.py resolve`, `bundle`, `inventory`, and `check` bind tasks to the
correct approved product/brand/surface. `bundle --task ID --write-lock` is an
explicit private write; `--refresh` is required to replace a lock after review.

`quality_gate.py --report FILE` validates review structure without model calls.
Exit 0 means ready for human review, 1 means blocked/inconclusive, 2 malformed input.
It never means approved to publish.

`connected_studio.py build|export` composes trusted project-local HTML with exact
registered assets. See [MEDIA.md](MEDIA.md). `connected_browser_smoke.py` tests the
fictional examples in inline-document mode; it does not test live URL navigation.
