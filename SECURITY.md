# Security policy

## Report privately
Use this repository's GitHub **Security → Report a vulnerability** once the
maintainer enables private reporting. If private reporting is unavailable, ask
for a private contact without publishing exploit details, secrets, or customer
data in an issue. Maintainers: enable private vulnerability reporting before a
public launch. This package does not invent a maintainer email address.

## Trust boundaries
Skills are instructions, not a sandbox. Host permissions, isolated execution,
branch protection, CI, and human authorization remain necessary. A malicious or
mistaken model can alter local records it can write. Hashes and local reports
help detect accidental drift; they are not tamper-proof attestations.

The installer only copies package files. It does not execute shell hooks,
install dependencies, open a browser, change authentication, modify AGENTS.md or
CLAUDE.md in your product, or change host permissions. Review code before use.
Never install from an untrusted pull request. Do not run test commands from an
untrusted repository on a machine holding production credentials.

Private context is git-ignored, not encrypted and not automatically excluded
from model processing. A hosted model receives the content your host sends.
Use sanitized summaries and synthetic fixtures. No automatic ingestion of mail,
customer databases, financial accounts, browser profiles, or secret files.

`run-check` executes an explicitly supplied command only with `--execute`.
It is not a sandbox and cannot guarantee its child process has no external
side effects. Review the command and its repository first. Logs can contain
secrets; keep evidence local and inspect it before sharing. The helper never
invokes a model CLI or switches authentication to an API key.

Media generation uses original local templates and text-only configuration.
Browser exports block remote requests. Do not use the exporter to render
arbitrary untrusted HTML; the bundled template is the supported input.

## Supported release
Version 1.x receives fixes on a best-effort community basis; there is no SLA or
security certification. Security-sensitive product changes still need review
appropriate to their risk. Follow the hard stops in the shared core contract.
