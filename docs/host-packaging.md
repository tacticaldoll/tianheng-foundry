# Host Packaging

The canonical skill content lives under `skills/`. Host manifests expose that same content without
forking the workflow:

| Host | Manifest |
|---|---|
| Codex | `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` |
| Claude | `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Gemini | `gemini-extension.json` |
| Generic agents | `distribution.json` |

Host adapters may describe discovery and packaging, but must not change eligibility, authority,
write boundaries, or proof requirements. Those belong in `SKILL.md` and its references.

All manifests share the distribution name and base release version. The Codex manifest may append a
local build suffix used to invalidate the installed plugin cache during development.

After changing a local Codex plugin, run the plugin-creator cachebuster helper against the source
repository and reinstall from the registered marketplace. Start a new thread before testing
discovery because active threads retain their loaded skill set.
