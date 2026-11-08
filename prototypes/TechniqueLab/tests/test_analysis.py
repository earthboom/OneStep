"""Offline retained-evidence checks, independent of ignored Unity builds."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

LAB = Path(__file__).resolve().parents[1]
SCRIPTS = ('analyze_results.py', 'analyze_dynamic.py', 'analyze_traffic.py', 'analyze_stream.py')
SUMMARIES = ('Results/summary.json', 'Results/Dynamic/summary.json', 'Results/Traffic/summary.json', 'Results/Stream/summary.json')


class OfflineAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='technique-analysis-', dir=os.environ.get('ONESTEP_TEST_ROOT'))
        cls.root = Path(cls.temp.name)
        repo = LAB.parents[1]
        tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', 'prototypes/TechniqueLab'], cwd=repo).decode().split('\0')
        for relative in filter(None, tracked):
            source = repo / relative
            if source.relative_to(LAB).parts[0] not in ('Assets', 'Results', 'ProjectSettings', 'Packages'):
                continue
            if source.name.lower().endswith('.kr.md') or source.suffix.lower() == '.png':
                continue
            target = cls.root / source.relative_to(LAB)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        # New untracked helper modules must also be usable before committing.
        for source in LAB.glob('*.py'):
            shutil.copy2(source, cls.root / source.name)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_analysis(self, script, *args):
        return subprocess.run([sys.executable, '-B', str(self.root / script), *args],
                              capture_output=True, text=True, encoding='utf-8', timeout=90)

    def result(self, run):
        self.assertTrue(run.stdout, run.stderr)
        return json.JSONDecoder().raw_decode(run.stdout.lstrip())[0]

    def test_offline_analysis_reports_missing_binaries_without_rewriting_history(self):
        before = {p: ((self.root/p).read_bytes(), (self.root/p).stat().st_mtime_ns) for p in SUMMARIES}
        for script in SCRIPTS:
            with self.subTest(script=script):
                run = self.run_analysis(script)
                self.assertEqual(run.returncode, 0, run.stderr)
                result = self.result(run)
                self.assertTrue(result['analysis_ok'])
                self.assertFalse(result['binary_verification']['complete'])
                self.assertTrue(all(c['status'] == 'missing' for c in result['binary_verification']['checks']))
        for p, (content, stamp) in before.items():
            self.assertEqual((self.root/p).read_bytes(), content)
            self.assertEqual((self.root/p).stat().st_mtime_ns, stamp)

    def test_strict_mode_fails_explicitly_for_missing_binaries(self):
        for script in SCRIPTS:
            with self.subTest(script=script):
                run = self.run_analysis(script, '--require-binaries')
                self.assertEqual(run.returncode, 1, run.stderr)
                result = self.result(run)
                self.assertTrue(result['analysis_ok'])
                self.assertTrue(result['binary_verification']['required'])
                self.assertFalse(result['binary_verification']['acceptable'])

    def test_output_is_opt_in_and_existing_evidence_cannot_be_overwritten(self):
        destination = self.root/'new-analysis.json'
        try:
            run = self.run_analysis('analyze_results.py', '--output', str(destination))
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(json.loads(destination.read_text(encoding='utf-8'))['analysis_ok'])
            before = destination.read_bytes()
            run = self.run_analysis('analyze_results.py', '--output', str(destination))
            self.assertEqual(run.returncode, 2, run.stderr)
            self.assertEqual(destination.read_bytes(), before)
        finally:
            destination.unlink(missing_ok=True)

    def test_present_wrong_binary_fails_even_without_strict_mode(self):
        player = self.root/'TrafficBuild/TrafficLab.exe'
        player.parent.mkdir(exist_ok=True)
        player.write_bytes(b'not the recorded player')
        try:
            run = self.run_analysis('analyze_traffic.py')
            self.assertEqual(run.returncode, 1, run.stderr)
            checks = self.result(run)['binary_verification']['checks']
            self.assertIn('mismatch', [c['status'] for c in checks])
        finally:
            player.unlink()

    def test_source_identity_mismatch_still_fails(self):
        source = self.root/'Assets/TechniqueLab/CameraDamping.cs'
        before = source.read_bytes()
        try:
            source.write_bytes(before + b'\n// modified after recorded run\n')
            run = self.run_analysis('analyze_traffic.py')
            self.assertNotEqual(run.returncode, 0)
        finally:
            source.write_bytes(before)

    def test_opt_in_summary_preserves_all_historical_metrics(self):
        for script, historical in zip(SCRIPTS, SUMMARIES):
            with self.subTest(script=script):
                destination = self.root/'comparison.json'
                try:
                    run = self.run_analysis(script, '--output', str(destination))
                    self.assertEqual(run.returncode, 0, run.stderr)
                    actual = json.loads(destination.read_text(encoding='utf-8'))
                    previous = json.loads((self.root/historical).read_text(encoding='utf-8'))
                    self.assertEqual({k: actual[k] for k in previous if k != 'ok'},
                                     {k: v for k, v in previous.items() if k != 'ok'})
                finally:
                    destination.unlink(missing_ok=True)

    def test_retained_behavior_failure_is_not_ignored_when_binaries_are_missing(self):
        report = self.root/'Results/Traffic/editor-final.json'
        original = report.read_bytes()
        try:
            data = json.loads(original.decode('utf-8-sig'))
            data['checks'][0]['passed'] = False
            report.write_text(json.dumps(data), encoding='utf-8')
            self.assertNotEqual(self.run_analysis('analyze_traffic.py').returncode, 0)
        finally:
            report.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
