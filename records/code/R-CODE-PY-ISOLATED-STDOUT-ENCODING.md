---
id: R-CODE-PY-ISOLATED-STDOUT-ENCODING
title: PYTHONIOENCODING had no effect on a Python script run in isolated mode
summary: Under python -I the interpreter ignores PYTHON* environment variables, so stdout stayed on the Windows console code page and text outside that code page raised UnicodeEncodeError. Select UTF-8 with the -X utf8 command-line option or write the output to a UTF-8 file.
kind: error
scope: CPython on Windows with a non-UTF-8 console code page; scripts started with -I or -E
keywords: [python, isolated-mode, "-I", "-E", PYTHONIOENCODING, PYTHONUTF8, "-X utf8", UTF-8-mode, cp949, UnicodeEncodeError, stdout-encoding, sys.flags.ignore_environment, Windows]
status: resolved
checked_at: 2026-11-24
context:
  platform: Windows 11, console code page 949
  python: "3.12.3"
trigger: Printing non-ASCII text from a script started with python -I, for example while reading downloaded or otherwise untrusted data in isolated mode
symptom: "UnicodeEncodeError: 'cp949' codec can't encode character, or unreadable text in captured output, although PYTHONIOENCODING=utf-8 is set for the command"
cause_status: confirmed
prevention: With -I or -E, select the output encoding on the command line (-X utf8) or write the result to a file opened with an explicit UTF-8 encoding; do not rely on PYTHON* environment variables
prevention_status: verified
---

## Expected and observed

A script that summarizes JSON containing Korean text and an em dash was started as `python -I` so that it would not import code from the data's directory. Setting `PYTHONIOENCODING=utf-8` in front of the command was expected to make `print` emit UTF-8. Observed: captured output was unreadable and the script stopped with `UnicodeEncodeError: 'cp949' codec can't encode character '—'`. The same error returned after the variable was added, which cost a second failed run.

## Cause and resolution

Isolated mode (`-I`) implies `-E`, which makes the interpreter ignore every `PYTHON*` environment variable, including `PYTHONIOENCODING` and `PYTHONUTF8`. Standard output therefore kept the console code page encoding. Confirmed on the affected machine: `PYTHONIOENCODING=utf-8 python -I -c "import sys; print(sys.stdout.encoding, sys.flags.ignore_environment)"` printed `cp949 1`.

Resolution used in the task: the script wrote its summary to a file opened with `encoding='utf-8'`, and the file was read afterwards. Command-line options are still honored in isolated mode, so `-X utf8` is the direct alternative.

## Recheck and prevention

On 2026-11-24, `python -I -X utf8 -c "import sys; print(sys.stdout.encoding); print('— ...')"` with Korean text printed `utf-8` and the expected UTF-8 bytes (checked with `od -c`), with no error. The file-output variant produced a readable UTF-8 summary in the same session.

Applies when isolation flags are required and the output contains characters outside the console code page. Without `-I` or `-E`, the environment variables work as documented and this record does not apply. `sys.stdout.reconfigure(encoding='utf-8')` inside the script is a plausible third option but was not run here.

## Evidence

- Session observation, 2026-11-24, Python 3.12.3 on Windows 11 with console code page 949: the failing run, the `cp949 1` probe and the passing `-X utf8` run described above.
- [Python command line documentation, option -I](https://docs.python.org/3/using/cmdline.html#cmdoption-I): isolated mode implies `-E`. [Option -E](https://docs.python.org/3/using/cmdline.html#cmdoption-E): ignore all `PYTHON*` environment variables. [Option -X utf8](https://docs.python.org/3/using/cmdline.html#cmdoption-X): enable UTF-8 mode. The documentation pages were not re-fetched in this session; the local probe is the checked evidence.
