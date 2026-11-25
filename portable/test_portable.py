"""Exercise the distributed files via the same entry points as end users."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
SKILL_DOC = re.compile(r"skills/vegabond-[^/]+/(?:SKILL\.md|references/[^/]+\.md)")


def web_sections(web):
    parts = re.split(r"^===== ([^\n]+?) =====\n\n", web, flags=re.MULTILINE)
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        # The builder inserts one separator newline immediately before each heading.
        if i + 2 < len(parts) and body.endswith("\n"):
            body = body[:-1]
        yield parts[i], body


def distribution_errors(source, zip_path, web):
    expected = {}
    for directory in (source / "skills").glob("vegabond-*"):
        for path in [directory / "SKILL.md", *(directory / "references").glob("*.md")]:
            if path.is_file() and not path.name.endswith(".kr.md"):
                expected[path.relative_to(source).as_posix()] = path.read_text(encoding="utf-8")

    def compare(label, entries):
        seen = set()
        errors = []
        for name, content in entries:
            if not SKILL_DOC.fullmatch(name):
                continue
            if name in seen:
                errors.append(f"{label} duplicate {name}")
            seen.add(name)
            if name not in expected:
                errors.append(f"{label} unexpected {name}")
            elif content != (expected[name].rstrip("\n") + "\n" if label == "web" else expected[name]):
                errors.append(f"{label} stale {name}")
        return errors + [f"{label} missing {name}" for name in sorted(expected.keys() - seen)]

    prefix = "onestep-strategy/"
    with ZipFile(zip_path) as archive:
        zipped = []
        for info in archive.infolist():
            if info.filename.startswith(prefix):
                name = info.filename[len(prefix):]
                if SKILL_DOC.fullmatch(name):
                    content = archive.read(info).decode("utf-8").replace("\r\n", "\n") if name in expected else None
                    zipped.append((name, content))
        errors = compare("ZIP", zipped)
    errors.extend(compare("web", web_sections(web)))
    return errors


class DistributionTests(unittest.TestCase):
    def test_each_format_matches_canonical_skills(self):
        web = (HERE / "OneStep-Web.txt").read_text(encoding="utf-8")
        errors = distribution_errors(HERE.parent, HERE / "OneStep-Project.zip", web)
        self.assertFalse(errors, "\n" + "\n".join(errors))

    def test_shared_omission_stale_and_duplicate_web_sections(self):
        entry = "skills/vegabond-image/SKILL.md"
        ref = "skills/vegabond-image/references/motion.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ref).parent.mkdir(parents=True)
            for name in (entry, ref):
                (root / name).write_text("current\n", encoding="utf-8")
            kit = root / "kit.zip"
            with ZipFile(kit, "w") as archive:
                archive.writestr("onestep-strategy/" + entry, b"current\r\n")
            web = f"===== {entry} =====\n\nold\n\n===== {entry} =====\n\ncurrent\n"
            self.assertCountEqual(distribution_errors(root, kit, web), [
                f"ZIP missing {ref}", f"web missing {ref}", f"web stale {entry}", f"web duplicate {entry}"])


class PortableKitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.kit = self.root / "unpacked kit"
        with ZipFile(HERE / "OneStep-Project.zip") as archive:
            archive.extractall(self.kit)
        self.project = self.root / "작업 폴더"
        self.project.mkdir()

    def install(self, code=0):
        process = subprocess.run(
            [sys.executable, str(self.kit / "install.py"), str(self.project)],
            cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        self.assertEqual(process.returncode, code, process.stdout)

    def test_move_without_original_kit(self):
        original = b"\xef\xbb\xbf# Local rules\r\nKeep this line."
        agent = self.project / "AGENTS.md"
        agent.write_bytes(original)
        self.install()
        merged = agent.read_bytes()
        self.assertTrue(merged.startswith(original))
        self.assertNotIn(b"\n", merged.replace(b"\r\n", b""))
        self.install()
        self.assertEqual(agent.read_bytes(), merged)
        relocated = self.root / "다른 위치"
        self.project.rename(relocated)
        shutil.rmtree(self.kit)
        for adapter in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            text = (relocated / adapter).read_text(encoding="utf-8-sig")
            for name in ("agents/vegabond-agent.md", "skills/vegabond-scout/SKILL.md"):
                relative = "onestep-strategy/" + name
                self.assertIn(relative, text)
                self.assertTrue((relocated / relative).is_file())
        folder = "skills/vegabond-image"
        strategy = relocated / "onestep-strategy"
        sections = dict(web_sections((HERE / "OneStep-Web.txt").read_text(encoding="utf-8")))
        for filename in ("stationery-characters.md", "2d-effects-and-motion.md"):
            target = f"references/{filename}"
            for body in ((strategy / folder / "SKILL.md").read_text(encoding="utf-8"), sections[f"{folder}/SKILL.md"]):
                self.assertIn(f"]({target})", body)
            expected = (HERE.parent / folder / target).read_text(encoding="utf-8")
            self.assertEqual((strategy / folder / target).read_text(encoding="utf-8"), expected)
            self.assertEqual(sections[f"{folder}/{target}"].rstrip("\n"), expected.rstrip("\n"))

    def test_conflicting_strategy_preserved(self):
        strategy = self.project / "onestep-strategy"
        strategy.mkdir()
        note = strategy / "notes.txt"
        note.write_bytes(b"User-owned data")
        self.install(code=1)
        self.assertEqual(note.read_bytes(), b"User-owned data")
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_manual_copy_and_web_sources_match(self):
        strategy = self.kit / "onestep-strategy"
        shutil.copytree(strategy, self.project / strategy.name)
        for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            shutil.copyfile(self.kit / name, self.project / name)
        web = (HERE / "OneStep-Web.txt").read_text(encoding="utf-8")
        for item in strategy.rglob("*.md"):
            relative = item.relative_to(strategy).as_posix()
            self.assertFalse(relative.endswith(".kr.md"))
            self.assertIn(f"===== {relative} =====\n\n" + item.read_text(encoding="utf-8").rstrip(), web)
        routed_references = {
            "code": ("cpp-project-guidelines.md", "cpp-implementation.md", "world-lifecycle-verification.md"),
            "code-design": ("world-lifecycle.md",),
        }
        for skill, filenames in routed_references.items():
            skill_root = self.project / strategy.name / f"skills/vegabond-{skill}"
            entry = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            for filename in filenames:
                relative = f"skills/vegabond-{skill}/references/{filename}"
                installed = self.project / strategy.name / relative
                self.assertTrue(installed.is_file(), relative)
                source = (HERE.parent / relative).read_text(encoding="utf-8")
                self.assertEqual(installed.read_text(encoding="utf-8"), source)
                self.assertIn(f"===== {relative} =====\n\n" + source.rstrip(), web)
                self.assertIn(f"](references/{filename})", entry)
                if filename.startswith("world-lifecycle"):
                    links = re.findall(r"\]\(([^)\s]+)\)", source)
                    for link in links:
                        if "://" in link:
                            continue
                        self.assertTrue((installed.parent / link.split("#", 1)[0]).is_file(), link)
        self.assertNotIn(str(HERE.parent), web)
        approved = {name for name in (HERE / "game-library.txt").read_text(encoding="utf-8").splitlines()
                    if name and not name.startswith("#")}
        details = {path.relative_to(strategy).as_posix()
                   for folder in ("knowledge", "records")
                   for path in (strategy / folder).rglob("*.md")
                   if path.name not in ("index.md", "sources.md")}
        self.assertEqual(details, approved)
        self.assertFalse((strategy / "knowledge/sources.local.json").exists())
        self.assertNotIn("SRC-NOVEL0-", (strategy / "knowledge/sources.md").read_text(encoding="utf-8"))
        for name in approved:
            entry = strategy / name
            content = entry.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)\s]+)\)", content):
                route, _, fragment = target.partition("#")
                if "://" in route or not route:
                    continue
                linked = (entry.parent / route).resolve()
                self.assertTrue(linked.is_file(), (name, target))
                if route.endswith("sources.md"):
                    self.assertIn("## " + fragment.upper() + "\n", linked.read_text(encoding="utf-8"))

    def test_keyword_lookup_after_relocation_and_in_web_upload(self):
        self.install()
        relocated = self.root / "게임 팀" / "New Project"
        relocated.parent.mkdir()
        self.project.rename(relocated)
        shutil.rmtree(self.kit)
        strategy = relocated / "onestep-strategy"
        web = (HERE / "OneStep-Web.txt").read_text(encoding="utf-8")
        segments = re.split(r"^===== (.+?) =====\n\n", web, flags=re.MULTILINE)
        sections = dict(zip(segments[1::2], segments[2::2]))
        for term, folder, ident in (
            ("메모리 풀링", "knowledge/code", "K-CODE-PERFORMANCE-MEASUREMENT"),
            ("GEOMETRY COLLECTION", "knowledge/game", "K-GAME-TECH-DESTRUCTION"),
            ("std::weak_ptr::lock", "knowledge/code", "K-CODE-RESOURCE-OWNERSHIP"),
            ("TVector::Equals", "records/code", "R-CODE-UE-TRANSFORM-TOLERANCE"),
            ("GIT_INDEX_FILE", "records/code", "R-CODE-GIT-INDEX-LOCK-RENAME"),
        ):
            with self.subTest(term=term):
                args = [sys.executable, "onestep-strategy/skills/vegabond-knowledge/scripts/search.py",
                        "search", "--project", "onestep-strategy", "--query", term,
                        "--domain", folder.split("/")[1], "--portable-library", "--limit", "3"]
                result = subprocess.run(args, cwd=relocated, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(ident, [hit["id"] for hit in json.loads(result.stdout)["results"]])
                row = next(line for line in sections[folder + "/index.md"].splitlines()
                           if line.startswith("| " + ident + " / "))
                detail = sections[f"{folder}/{ident}.md"]
                self.assertIn(term.casefold(), (row + detail).casefold())
                self.assertIn("## Evidence", detail)
        self.assertFalse((strategy / ".cache").exists())

    def test_non_utf8_entry_fails_before_first_write(self):
        entry = self.project / "GEMINI.md"
        original = "# Existing".encode("utf-16")
        entry.write_bytes(original)
        self.install(code=1)
        self.assertEqual(entry.read_bytes(), original)
        self.assertEqual(list(self.project.iterdir()), [entry])


if __name__ == "__main__":
    unittest.main(verbosity=2)
