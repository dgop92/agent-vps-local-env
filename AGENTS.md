# AGENTS.md

This repo is Ansible playbooks for setting up an Ubuntu 24 VPS: installing developer
tooling and configuring the machine. It is meant to be cloned onto the VPS and run
there — never run these playbooks on a local development machine.

## Structure

- `playbooks/` — Ansible playbooks, one tool/concern per file (e.g. `install_mise.yml`).
- `ansible.cfg` — Ansible configuration (`retry_files_enabled = False`).
- `scripts/` — standalone `uv` scripts (PEP 723 inline deps) for local tasks that
  aren't part of the VPS setup itself, e.g. validation.

## Validation

Before considering a playbook change done, validate it with:

```bash
uv run scripts/validate.py
```

This YAML-parses every file in `playbooks/` and reports which ones fail — it does not
run Ansible itself (a full `ansible-playbook --syntax-check` needs Ansible installed
and should be run on the actual target VPS, not locally). Never execute a playbook
(`ansible-playbook playbooks/<name>.yml`) from this local machine.

## Conventions

- Playbooks target `hosts: localhost` with `connection: local` — they configure the
  machine they run on (the VPS), not remote hosts.
- Tasks that install a tool check whether it's already present before installing, so
  playbooks are safe to re-run (see `install_mise.yml` as the pattern to follow).
- This repo targets Ubuntu 24 specifically — assume `apt`/Debian conventions and a
  `bash` login shell (`~/.bashrc`), not macOS/Homebrew or zsh.
