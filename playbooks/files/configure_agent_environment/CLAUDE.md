# Agent VPS Environment

You are running as Claude Code on a dedicated Ubuntu 24 VPS provisioned for
autonomous agent work — not a developer's personal laptop. Human oversight
here is minimal: the user mainly checks in from a mobile phone, not a
terminal sitting next to you, so don't expect a quick response if you ask
something — but also don't block on asking when you genuinely need to.

- Your workspace is `~/workspace` — clone repos and do work there.
- Permission prompts are bypassed by default on this machine
  (`permissions.defaultMode: bypassPermissions`) — act accordingly: you are
  trusted to act autonomously, so be deliberate and careful before running
  destructive or irreversible commands, since no human will be prompted to
  confirm.
- This environment is expected to work out of the box. If the same operation
  fails repeatedly, the cause is likely a missing dependency or piece of
  environment setup — stop retrying and ask the user rather than working
  around it silently.
- You are not a root user and do not know the sudo password. Installing new
  system packages or tooling requires user intervention — ask rather than
  attempting workarounds like sudo, manual binary downloads to bypass a
  package manager, etc.
