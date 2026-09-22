# Host compatibility and authentication

Checked against official documentation on 2026-09-23. Host products evolve; verify
paths and invocation in current documentation when updating. No authenticated
Codex/Claude session was available for live host testing in the build environment.

| Host | User skills | Project skills | Explicit entry |
|---|---|---|---|
| Codex CLI / IDE | `~/.agents/skills` | `.agents/skills` | `$co-founder` / skill picker |
| Claude Code | `~/.claude/skills` | `.claude/skills` | `/co-founder` |

Sources: [Codex skills](https://developers.openai.com/codex/skills/),
[Claude Code skills](https://code.claude.com/docs/en/skills),
[Agent Skills specification](https://agentskills.io/specification).
The latest desktop skill picker may differ from CLI/IDE invocation. This package
uses folder-based installation, not a marketplace/plugin installation claim.

## Installation-manager paths

The table above describes this pack's existing Python manager configuration. The
external skills CLI can use a canonical folder plus host-specific links; its Codex
user-level destination may differ. Follow the actual CLI summary and current host
documentation, and check both locations for duplicate versions. The package does
not claim that all historical CLI and host versions use identical paths.
See [installation](INSTALLATION.md) for switching managers without overwriting
customized skills or deleting private product context.

## Billing boundary

[Codex authentication](https://developers.openai.com/codex/auth/) distinguishes
subscription sign-in from API-key authentication. Check `codex login status`.
[Claude authentication](https://code.claude.com/docs/en/authentication) describes
its supported authentication methods; use `/status` to inspect your session.
`doctor` reports only relevant environment-variable names, never their values,
and cannot prove which account or billing path the host is currently using.

No helper reads host auth files, extracts subscription tokens, calls model APIs,
or invokes undocumented provider endpoints. Installing this pack does not increase
your allowance, change model quality, bypass limits or make model work free.

## Permissions

Keep the host's sandbox/approval controls. No `allowed-tools`, bypass-permissions,
auto-deploy hook or persistent scheduler is installed. See
[Claude permissions](https://code.claude.com/docs/en/permissions).
External text and tool results remain untrusted inputs. The local gate cannot
independently prevent the same agent from editing its own evidence.

## Portability

One shared core with thin optional wrappers. Plain Markdown/JSON/Python; no model
SDK, mandatory vector database or always-running server. Capabilities such as web
search, browser access, connected email and image generation depend on the host.
The skill must report missing access instead of fabricating work. A fresh task
uses the same approved project records in either host; conversation memory is not
automatically transferred between providers.
