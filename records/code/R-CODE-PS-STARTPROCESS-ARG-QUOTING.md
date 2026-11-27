---
id: R-CODE-PS-STARTPROCESS-ARG-QUOTING
title: Start-Process split an argument that contained spaces, so the launched program received a truncated option
summary: PowerShell Start-Process joins -ArgumentList elements with spaces without quoting them, so an element such as -TestExit="Automation Test Queue Empty" written without embedded quotes arrived as several arguments. Embed the double quotes in each element that contains spaces and check the command line the program logged.
kind: error
scope: Windows PowerShell 5.1 and PowerShell 7 Start-Process launching native programs whose options contain spaces
keywords: [PowerShell, Start-Process, ArgumentList, quoting, double quotes, spaces in arguments, command line, native executable, UnrealEditor-cmd.exe, "-ExecCmds", "-TestExit", headless automation, LogInit Command Line]
status: resolved
checked_at: 2026-11-24
context:
  platform: Windows 11
  shell: "PowerShell 7"
trigger: Launching a native executable with Start-Process -ArgumentList where an option value contains spaces, for example an Unreal editor automation run with -ExecCmds and -TestExit
symptom: The launched program behaves as if an option were cut at its first space; an Unreal editor automation run exited near frame 0 without running the test, and its log showed -TestExit=Automation followed by stray words
cause_status: confirmed
prevention: Put escaped double quotes around each option value that contains spaces inside its -ArgumentList element, then compare the program's own logged command line with the intended one before trusting the run
prevention_status: verified
---

## Expected and observed

A script launched an Unreal editor automation run with `Start-Process -ArgumentList @(...)`, where one element was `-ExecCmds=Automation RunTests <name>` and another was the exit condition text with spaces. Expected: the editor ran the test and quit when the queue emptied. Observed: the editor quit almost immediately, no test result was reported, and the logged command line contained the options broken at each space, for example `-TestExit=Automation`.

## Cause and resolution

`Start-Process` builds one command-line string by joining the `-ArgumentList` elements with spaces and does not add quotes around an element that contains spaces. The receiving program then tokenizes that string, so one intended option became several. Confirmed by the program's own logged command line in the failing run.

Resolution: each element whose value contains spaces carries its own quotes, for example ``"-ExecCmds=`"Automation RunTests $Tests`""`` and `'-TestExit="Automation Test Queue Empty"'`, and paths with spaces are quoted the same way. The next run executed the test and reported its result.

## Recheck and prevention

On 2026-11-24 the corrected run's `LogInit: Command Line:` line showed each option intact and the run ended with the automation result line. Comparing that logged line with the intended arguments is the check that exposed the original failure.

Applies to `Start-Process`. Invoking the executable directly with the call operator `&` passes array elements as separate arguments with its own quoting rules, which were not examined here. A program's exit code alone did not reveal the problem.

## Evidence

- Session observation, 2026-11-24, PowerShell 7 on Windows 11: the failing launch, its logged command line, and the corrected launch described above.
- [Start-Process documentation, ArgumentList parameter](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process): arguments containing spaces must be wrapped in escaped double quotes. The page was not re-fetched in this session; the logged command lines are the checked evidence.
