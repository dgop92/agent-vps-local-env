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

## Recommended Workflow

`configure_agent_environment.yml` is not part of `do_it_all.yml` because it needs a couple of
manual authentication steps in between. The suggested order is:

1. Run `do_it_all.yml` first to install base tooling (ripgrep, Claude Code, mise, gh):

   ```bash
   ansible-playbook playbooks/do_it_all.yml -K
   ```

2. Log in to Claude Code manually (this step can't be automated — it needs a device-code
   login flow completed in a browser):

   - Run `claude` on the VPS. Since there's no browser on the VPS itself, it will print a
     login URL and a code instead of opening a browser directly.
   - On another machine (e.g. your phone), open that URL and complete the login there.
   - Copy the code shown back on the VPS, then paste it into the terminal prompt on the
     VPS to finish logging in.

3. Authenticate `gh` manually (this step can't be automated — it needs a token you
   generate yourself):

   - Create a GitHub fine-grained Personal Access Token at
     https://github.com/settings/personal-access-tokens/new
   - Authenticate with it:

     ```bash
     echo "YOUR_GITHUB_FINE_GRAINED_PAT" | gh auth login --with-token
     ```

4. Run `configure_agent_environment.yml` to finish setting up the agent's working
   environment (workspace folder, Claude Code permissions, user-level `CLAUDE.md`,
   the `mattpocock/skills` plugin, git identity, and git's credential helper):

   ```bash
   ansible-playbook playbooks/configure_agent_environment.yml
   ```
