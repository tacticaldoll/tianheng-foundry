from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from th_foundry_cli import cli


class ThFoundryCliTests(unittest.TestCase):
    def test_workspace_version_falls_back_to_workspace_manifest(self) -> None:
        manifest = json.loads(
            (cli.WORKSPACE_ROOT / "distribution.json").read_text(encoding="utf-8")
        )

        with patch.object(cli, "version", side_effect=cli.PackageNotFoundError):
            self.assertEqual(cli.workspace_version(), manifest["version"])

    def test_installed_cli_uses_build_metadata_version(self) -> None:
        with patch.object(cli, "version", return_value="9.8.7"):
            self.assertEqual(cli.workspace_version(), "9.8.7")

    def test_policy_contains_only_tianheng_foundry_distribution_choices(self) -> None:
        self.assertEqual(cli.FOUNDRY_POLICY.identity, "tianheng-foundry")
        self.assertEqual(cli.FOUNDRY_POLICY.prefix, "tianheng-foundry-")
        self.assertEqual(
            cli.FOUNDRY_POLICY.provenance_file, ".tianheng-foundry-install.json"
        )

    def test_main_binds_workspace_version_and_policy_without_a_fixed_source(self) -> None:
        with patch.object(cli, "engine_main", return_value=0) as engine:
            self.assertEqual(cli.main(["hosts"]), 0)

        self.assertEqual(engine.call_args.args, (["hosts"],))
        self.assertEqual(engine.call_args.kwargs["program"], "th-foundry")
        self.assertEqual(engine.call_args.kwargs["version"], cli.workspace_version())
        self.assertIs(engine.call_args.kwargs["distribution_policy"], cli.FOUNDRY_POLICY)
        self.assertIsNone(engine.call_args.kwargs["source_provider"])


if __name__ == "__main__":
    unittest.main()
