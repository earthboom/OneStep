"""Shared, read-only evidence verification; never silently replace archived summaries."""
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re


def parse_options(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-binaries', action='store_true',
                        help='Fail when any declared binary is missing, as well as on mismatches.')
    parser.add_argument('--binary-root', type=Path,
                        help='Root of an archived build tree; defaults to this lab directory.')
    parser.add_argument('--output', type=Path, help='Write full JSON to a NEW file; never overwrite.')
    options = parser.parse_args(argv)
    if options.output is not None and (options.output.exists() or options.output.is_symlink()):
        parser.error('--output must name a new file; existing evidence is never overwritten')
    return options


def add_expected(expected, relative, digest):
    """Reject inconsistent run manifests rather than taking the last digest."""
    path = Path(relative)
    if (path.anchor or PureWindowsPath(relative).drive or '..' in path.parts
            or '\\' in relative or not path.parts or str(path) == '.'):
        raise ValueError('Expected binary path must stay relative to the binary root: ' + relative)
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
        raise ValueError('Invalid SHA-256 for ' + relative)
    digest = digest.upper()
    if relative in expected and expected[relative] != digest:
        raise ValueError('Conflicting run-manifest binary hashes for ' + relative)
    expected[relative] = digest


def verify_binaries(root, expected, require=False):
    """Missing is explicit and optional; present but wrong/unreadable is always a failure."""
    root = Path(root).resolve()
    checks = []
    for relative, digest in expected.items():
        # Validate even callers that did not use add_expected.
        add_expected({}, relative, digest)
        row = dict(path=relative, expected_sha256=digest.upper(), observed_sha256=None)
        try:
            target = (root / relative).resolve()
            if not target.is_relative_to(root):
                row.update(status='unavailable', reason='Resolved path leaves binary root')
            else:
                with target.open('rb') as source:
                    sha = hashlib.sha256()
                    for block in iter(lambda: source.read(1024 * 1024), b''):
                        sha.update(block)
                row['observed_sha256'] = sha.hexdigest().upper()
                row['status'] = 'matched' if row['observed_sha256'] == row['expected_sha256'] else 'mismatch'
        except FileNotFoundError:
            row.update(status='missing', reason='Recorded binary is not available at this root')
        except OSError as error:
            row.update(status='unavailable', reason=str(error))
        checks.append(row)
    complete = bool(checks) and all(c['status'] == 'matched' for c in checks)
    acceptable = bool(checks) and all(c['status'] == 'matched' or
                                    (c['status'] == 'missing' and not require) for c in checks)
    return dict(required=require, complete=complete, acceptable=acceptable, root=str(root),
                scope='Only the binary paths declared by this analyzer; no new engine execution or full build certification.',
                checks=checks)


def emit_summary(summary, options, root, expected, omit=()):
    report = {k: v for k, v in summary.items() if k != 'ok'}
    report['analysis_ok'] = True
    report['binary_verification'] = verify_binaries(options.binary_root or root, expected,
                                                   options.require_binaries)
    if options.output is not None:
        try:
            with options.output.open('x', encoding='utf-8') as target:
                target.write(json.dumps(report, indent=2) + '\n')
        except OSError as error:
            raise SystemExit('Cannot create new analysis output: ' + str(error)) from error
    print(json.dumps({k: v for k, v in report.items() if k not in omit}, indent=2))
    return 0 if report['binary_verification']['acceptable'] else 1
