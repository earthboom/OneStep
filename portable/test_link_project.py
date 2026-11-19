"""Exercise live checkout links through Git and the public setup command."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENTRY = Path("agents/vegabond-agent.md")
POINTER = Path(".onestep/checkout.local.json")


class LinkedProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.origin = self.base / "upstream"
        self.origin.mkdir()
        for name in (ENTRY, Path("link_project.py"), Path("skills/vegabond-scout/SKILL.md"),
                     Path("knowledge/game/index.md"), Path("knowledge/code/index.md"),
                     Path("records/code/index.md")):
            dest = self.origin / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        self.git(self.origin, "init", "-q")
        self.git(self.origin, "add", ".")
        self.commit()
        self.checkout = self.base / "AI 자료"
        self.git(self.base, "clone", "-q", str(self.origin), str(self.checkout))
        self.project = self.base / "게임 프로젝트"
        self.project.mkdir()

    def git(self, cwd, *args):
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True)

    def commit(self):
        self.git(self.origin, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qam", "fixture")

    def link(self, project, *args, ok=True):
        run = subprocess.run([sys.executable, str(self.checkout / "link_project.py"), str(project), *args],
                             cwd=self.base, capture_output=True)
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        return run.stdout

    def test_shared_pull_across_projects_and_new_pc(self):
        sibling = self.base / "소설"
        sibling.mkdir()
        self.git(self.project, "init", "-q")
        original = b"\xef\xbb\xbf# Team instructions\r\nOriginal line\r\n"
        (self.project / "CLAUDE.md").write_bytes(original)
        for target in (self.project, sibling):
            self.link(target)
            self.link(target, "--check")
            self.assertIn(b"0 files updated", self.link(target))
        self.git(self.project, "check-ignore", "--quiet", POINTER.as_posix())
        self.assertTrue((self.project / "CLAUDE.md").read_bytes().startswith(original))
        for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            self.assertIn(POINTER.as_posix(), (self.project / name).read_text(encoding="utf-8-sig"))
        with (self.origin / ENTRY).open("a", encoding="utf-8") as out:
            out.write("\nUpdated upstream fixture\n")
        self.commit()
        self.git(self.checkout, "pull", "--ff-only")
        for target in (self.project, sibling):
            source = json.loads((target / POINTER).read_text(encoding="utf-8"))["checkout"]
            self.assertIn("Updated upstream fixture", (target / source / ENTRY).read_text(encoding="utf-8"))
            self.assertFalse((target / "onestep-strategy").exists())
        self.git(self.project, "add", ".")
        self.git(self.project, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", "shared instructions")
        other_pc = self.base / "other PC"
        other_pc.mkdir()
        self.git(other_pc, "clone", "-q", str(self.project), "game")
        self.git(other_pc, "clone", "-q", str(self.origin), "OneStep")
        self.checkout = other_pc / "OneStep"
        target = other_pc / "game"
        self.assertFalse((target / POINTER).exists())
        self.link(target, "--check")

    def test_migrate_zip_relink_and_preserve_custom_files(self):
        from build import ADAPTER
        rule = self.project / "GEMINI.md"
        rule.write_text("# Custom\n" + ADAPTER + "\nKeep this too.", encoding="utf-8")
        (self.project / "AGENTS.override.md").write_text("My override", encoding="utf-8")
        self.link(self.project)
        text = rule.read_text(encoding="utf-8")
        self.assertNotIn("onestep-strategy/agents/", text)
        self.assertIn("Keep this too.", text)
        self.assertIn(POINTER.as_posix(), (self.project / "AGENTS.override.md").read_text(encoding="utf-8"))
        moved = self.base / "새 위치"
        self.checkout.rename(moved)
        self.checkout = moved
        self.link(self.project, "--check", ok=False)
        self.link(self.project)
        self.link(self.project, "--check")

    def test_invalid_entry_aborts_before_writing(self):
        (self.project / "GEMINI.md").write_bytes(b"\xff\xfeX\x00")
        self.link(self.project, ok=False)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / POINTER).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
