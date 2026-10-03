import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "preflight.py"
SPEC = importlib.util.spec_from_file_location("preflight", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.settings = self.root / ".product-atlas.json"
        self.source = self.root / "application"
        self.source.mkdir()
        self.code = self.source / "cancel.py"
        self.code.write_text("def can_cancel(order):\n    return not order.dispatched\n")
        self.config = {
            "schema_version": 2,
            "product": "Orders",
            "sources": [{"id": "app", "kind": "code", "path": "application"}],
            "paths": {name: "product/" + name for name in MODULE.STORES},
        }

    def run_check(self):
        self.settings.write_text(json.dumps(self.config))
        return MODULE.preflight(self.settings)

    def test_relative_paths_use_settings_location_and_check_is_read_only(self):
        result = self.run_check()
        self.assertEqual(result["sources"][0]["files"], [str(self.code)])
        self.assertEqual(result["paths"]["documentation"], str(self.root / "product/documentation"))
        self.assertFalse((self.root / "product").exists())

    def test_version_one_settings_decline_without_modifying_project_data(self):
        self.config["schema_version"] = 1
        self.config["paths"] = {
            "intent": "product/intent", "questions": "product/questions",
            "generation": "product/generation", "wiki": "product/wiki",
        }
        old_output = self.root / "product/wiki"
        old_output.mkdir(parents=True)
        page = old_output / "index.md"
        page.write_text("Existing output")
        with self.assertRaisesRegex(ValueError, "references/upgrade.md"):
            self.run_check()
        self.assertEqual(page.read_text(), "Existing output")
        self.assertEqual(json.loads(self.settings.read_text()), self.config)

    def test_shipped_template_uses_current_schema_and_directory_names(self):
        template = SCRIPT.parents[1] / "templates" / "product-atlas.json"
        self.config = json.loads(template.read_text())
        self.config["sources"] = [{"id": "app", "kind": "code", "path": "application"}]
        result = self.run_check()
        self.assertEqual(result["paths"], {
            name: str(self.root / "product" / name)
            for name in ("intent", "questions", "history", "documentation")
        })

    def test_documentation_alone_qualifies(self):
        self.config["sources"] = [{"id": "docs", "kind": "documentation", "path": "requirements.md"}]
        (self.root / "requirements.md").write_text("Buyers can cancel before dispatch.\n")
        self.assertEqual(self.run_check()["status"], "candidates-found")

    def test_pdf_corpus_is_offered_to_agent_for_content_extraction(self):
        self.config["sources"] = [{"id": "docs", "kind": "documentation", "path": "requirements.pdf"}]
        document = self.root / "requirements.pdf"
        document.write_bytes(b"%PDF-1.7\n%\x80\x81\x82\x83\n")
        self.assertEqual(self.run_check()["sources"][0]["files"], [str(document)])

    def test_utf8_sampling_does_not_reject_a_split_character(self):
        self.code.write_text("a" * 8191 + "\u00e9\n", encoding="utf-8")
        self.assertEqual(self.run_check()["sources"][0]["files"], [str(self.code)])

    def test_empty_and_binary_only_corpus_declines(self):
        for contents in (b"", b"  \n", b"\x00\xff"):
            with self.subTest(contents=contents):
                self.code.write_bytes(contents)
                with self.assertRaisesRegex(ValueError, "No readable code or documentation"):
                    self.run_check()

    def test_feedback_alone_does_not_replace_required_corpus(self):
        self.config["sources"][0]["kind"] = "feedback"
        with self.assertRaisesRegex(ValueError, "No readable code or documentation"):
            self.run_check()

    def test_generated_and_registry_files_do_not_bootstrap_a_corpus(self):
        self.code.unlink()
        self.config["sources"][0]["path"] = "."
        for value in self.config["paths"].values():
            path = self.root / value
            path.mkdir(parents=True)
            (path / "existing.md").write_text("This must not count as evidence.\n")
        for name in (".product-atlas-stage-example", ".product-atlas-backup-example"):
            path = self.root / name
            path.mkdir()
            (path / "index.md").write_text("Staged or old output is not evidence.\n")
        with self.assertRaisesRegex(ValueError, "No readable code or documentation"):
            self.run_check()

    def test_documentation_cannot_contain_sources_or_settings(self):
        for value in ("application", "."):
            with self.subTest(path=value):
                self.config["paths"]["documentation"] = value
                with self.assertRaises(ValueError):
                    self.run_check()

    def test_nested_registries_are_rejected(self):
        self.config["paths"]["questions"] = "product/documentation/questions"
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.run_check()

    def test_symlink_cannot_disguise_overlap(self):
        (self.root / "product/documentation").mkdir(parents=True)
        (self.root / "alias").symlink_to(self.root / "product/documentation", target_is_directory=True)
        self.config["paths"]["intent"] = "alias"
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.run_check()

    def test_source_scan_excludes_archives_secrets_and_symlinks(self):
        hidden = self.source / "archive"
        hidden.mkdir()
        (hidden / "old.md").write_text("Old policy\n")
        (self.source / ".env").write_text("PLACEHOLDER=not-a-secret\n")
        (self.source / "alias.md").symlink_to(self.code)
        self.assertEqual(self.run_check()["sources"][0]["files"], [str(self.code)])

    def test_duplicate_ids_and_missing_sources_fail(self):
        self.config["sources"].append(dict(self.config["sources"][0]))
        with self.assertRaisesRegex(ValueError, "unique"):
            self.run_check()
        self.config["sources"] = [{"id": "gone", "kind": "code", "path": "missing"}]
        with self.assertRaisesRegex(ValueError, "does not exist"):
            self.run_check()

    def test_existing_documentation_is_preserved_on_failure(self):
        documentation = self.root / "product/documentation"
        documentation.mkdir(parents=True)
        page = documentation / "index.md"
        page.write_text("Previous valid documentation\n")
        self.code.unlink()
        with self.assertRaises(ValueError):
            self.run_check()
        self.assertEqual(page.read_text(), "Previous valid documentation\n")

    def test_output_cannot_be_a_git_checkout(self):
        documentation = self.root / "product/documentation"
        documentation.mkdir(parents=True)
        (documentation / ".git").write_text("gitdir: /placeholder\n")
        with self.assertRaisesRegex(ValueError, "Git checkout"):
            self.run_check()

    def test_cli_returns_json_error_and_nonzero_status(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--settings", str(self.root / "absent.json")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stderr)["status"], "error")
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
