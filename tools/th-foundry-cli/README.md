# th-foundry CLI

The `th-foundry` command is a thin Tianheng Foundry policy adapter over
[`agent-skill-deployer`](https://github.com/tacticaldoll/agent-skill-deployer). The engine owns
host discovery, inventory, deployment channels, provenance, reconciliation, and verification. This
package owns only the command name, namespace, provenance identity, and validators.

## How this differs from Fornax's CLI

Fornax's own `fornax` command fixes a `source_provider`: every deploy resolves a tagged, pushed
release and refuses a local `--source`. That is a deliberate formal-release-only policy, appropriate
for a published, versioned tool.

Tianheng Foundry has not cut a tagged release yet, so `th-foundry` leaves `source_provider` unset.
It deploys from a local checkout instead — resolved from `--source PATH`, a configured default
(`th-foundry config --source PATH`), or the current directory when it contains a `skills/` folder.
Native plugin hosts (Claude, Codex) still require a clean working tree and a valid remote origin
URL before deploying (`Source.require_formal_checkout`) — just not a matching git tag. Revisit this
binding once the project starts cutting tagged releases; at that point it can adopt the same
`GitRelease`-backed `source_provider` Fornax uses.

## Install the command

```sh
uv tool install /path/to/tianheng-foundry/tools/th-foundry-cli
th-foundry deploy --dry-run
th-foundry deploy --all
```

## Run without installing

```sh
uvx --from /path/to/tianheng-foundry/tools/th-foundry-cli th-foundry deploy --all
```

## Commands

```sh
th-foundry hosts
th-foundry status
th-foundry doctor
th-foundry deploy --dry-run
th-foundry deploy --all
th-foundry config --source /path/to/tianheng-foundry
```

Installed skills on directory-discovery hosts (Antigravity, Copilot, Cline, Cursor, OpenCode) are
managed copies namespaced `tianheng-foundry-<skill>` with a `.tianheng-foundry-install.json`
provenance file; none link back to the workspace. Native plugin hosts (Claude Code, Codex) install
through their own CLI's marketplace/plugin lifecycle.

## Development

```sh
PYTHONPATH=/path/to/agent-skill-deployer:tools/th-foundry-cli \
  python3 -m unittest discover -s tools/th-foundry-cli/tests -v
```
