# Host compatibility and subscription use

Sources checked 2026-09-23: [Codex skills](https://developers.openai.com/codex/skills/),
[Codex authentication](https://developers.openai.com/codex/auth/),
[Claude Code skills](https://code.claude.com/docs/en/skills), and
[Claude authentication](https://code.claude.com/docs/en/authentication).

Codex discovers user skills in `~/.agents/skills` and project skills under
`.agents/skills`. Claude Code uses `~/.claude/skills` or `.claude/skills`.
The installer copies the shared entry folder, and optional specialist wrappers,
into those documented locations. It changes no host settings and grants no tools.

Use supported subscription login in the relevant host. Codex: `codex login status`
checks the authentication method. Claude Code: inspect `/status`. A configured API
key/provider override can change billing; do not print its value or assume that a
subscription is active solely because it exists. The doctor reports presence of
relevant environment-variable names, not secrets or active billing verification.

Default lite mode exposes one entry skill containing all twelve workflow files.
Full mode also exposes twelve named specialist skills. Their shared dependency
must remain installed alongside them. Restart/reload the host if discovery does
not update. Do not install both user and project copies with the same name unless
you intentionally manage that precedence; duplicate discovery can be confusing.

Keep baseline host sandbox/approval controls. The package does not grant broad
allowed-tools, use a forked agent, change model/effort, or bypass permissions.
It cannot increase your subscription quota or read the provider's remaining
allowance. Live host discovery/behavior must be smoke-tested by a subscribed user.
