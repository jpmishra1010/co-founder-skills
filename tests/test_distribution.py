"""Offline distribution checks. These do not execute or impersonate the skills CLI."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from _load import ROOT


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.pack = self.base / "installed" / "co-founder"
        shutil.copytree(ROOT / "skills" / "co-founder", self.pack,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.env = os.environ.copy()
        self.env.pop("PYTHONPATH", None)
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def tearDown(self):
        self.temp.cleanup()

    def run_helper(self, name, *args):
        return subprocess.run(
            [sys.executable, str(self.pack / "scripts" / name), *args],
            cwd=self.base, env=self.env, capture_output=True, text=True,
            timeout=20, check=False,
        )

    def test_core_metadata_discoverable(self):
        text = (self.pack / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, r"(?m)^name: co-founder$")
        self.assertRegex(text, r"(?m)^description: .+")

    def test_core_contains_all_workflows(self):
        names = json.loads((ROOT / "manifest.json").read_text())["specialists"]
        self.assertEqual(12, len(names))
        for name in names:
            self.assertTrue((self.pack / "workflows" / f"{name}.md").is_file())
            self.assertTrue((self.pack / "references" / "principles" / f"{name}.md").is_file())

    def test_core_markdown_links_stay_inside_installed_skill(self):
        for file in self.pack.rglob("*.md"):
            text = file.read_text(encoding="utf-8")
            for link in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                    continue
                target = (file.parent / link.split("#", 1)[0]).resolve()
                self.assertTrue(target.is_relative_to(self.pack), f"External file dependency: {file}: {link}")
                self.assertTrue(target.exists(), f"Missing local target: {file}: {link}")

    def test_license_travels_with_every_skill(self):
        expected = (ROOT / "LICENSE").read_bytes()
        for directory in (ROOT / "skills").iterdir():
            self.assertEqual(expected, (directory / "LICENSE").read_bytes())
        self.assertTrue((self.pack / "NOTICE.md").is_file())

    def test_helper_help_without_repository_root(self):
        for script in sorted((self.pack / "scripts").glob("*.py")):
            result = self.run_helper(script.name, "--help")
            self.assertEqual(0, result.returncode, f"{script.name}: {result.stderr}")

    def test_project_initialization_without_repository_root(self):
        product = self.base / "sample-product"
        product.mkdir()
        result = self.run_helper("cf.py", "init", "--project", str(product))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((product / ".co-founder" / "project.json").is_file())
        self.assertTrue((product / ".co-founder" / "brand.json").is_file())

    def test_wrapper_dependencies_documented_and_available(self):
        names = json.loads((ROOT / "manifest.json").read_text())["specialists"]
        for name in names:
            wrapper = ROOT / "skills" / f"co-founder-{name}" / "SKILL.md"
            text = wrapper.read_text(encoding="utf-8")
            self.assertIn("shared co-founder folder must be installed", text)
            self.assertTrue((self.pack / "workflows" / f"{name}.md").is_file())


if __name__ == "__main__":
    unittest.main()
