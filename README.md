# Agent VPS Local Env

Ubuntu VSP Machine setup, managed with Ansible

## Prerequisites

Ansible must be installed on the VPS before running any playbook. Install it via `apt`:

```bash
sudo apt update
sudo apt install -y ansible
```

## Usage

Run a playbook with:

```bash
ansible-playbook playbooks/<playbook>.yml
```

To run every playbook in order (ripgrep, Claude Code, mise, gh), use the combined playbook:

```bash
ansible-playbook playbooks/do_it_all.yml
```

### Playbooks that require `become: true`

Some playbooks install system packages via `apt` and need root privileges for those tasks
(`become: true`). Currently these are:

- `install_ripgrep.yml`
- `install_gh.yml`

When running one of these (directly or via `do_it_all.yml`), pass a flag so Ansible can escalate
privileges:

```bash
ansible-playbook playbooks/install_ripgrep.yml --ask-become-pass
# or the shorthand:
ansible-playbook playbooks/install_ripgrep.yml -K
```

This prompts once for the `sudo` password before the play starts. If the VPS already has
passwordless `sudo` configured for the user running Ansible, `--ask-become-pass`/`-K` can be
omitted.

The remaining playbooks (`install_claude_code.yml`, `install_mise.yml`) install tools into user
space (e.g. `~/.local/bin`) and don't need `become` or a sudo password.

`do_it_all.yml` chains all four playbooks together, so run it with `--ask-become-pass`/`-K` to
cover the ripgrep and gh installs within it.
