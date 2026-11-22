[CmdletBinding()]
param(
    [switch]$Build,
    [ValidateRange(0, 50)][int]$Runs = 3,
    [switch]$NoGraphics,
    [string]$Unity = 'C:\Program Files\Unity\Hub\Editor\6000.0.77f1\Editor\Unity.exe'
)

$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$work = Join-Path $project 'Work'
$player = Join-Path $project 'Build/WorldLifecycle.exe'
$legacy = (Resolve-Path (Join-Path $project '../fixtures/legacy-v1.json')).Path
New-Item -ItemType Directory -Path $work -Force | Out-Null

function Invoke-OwnedProcess([string]$Executable, [string[]]$Arguments, [int]$TimeoutSeconds) {
    $child = Start-Process -FilePath $Executable -ArgumentList $Arguments -WorkingDirectory $project -WindowStyle Hidden -PassThru
    if (!$child.WaitForExit($TimeoutSeconds * 1000)) {
        Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue
        throw "Process $($child.Id) exceeded ${TimeoutSeconds}s. See logs in $work."
    }
    if ($child.ExitCode -ne 0) {
        throw "Process $($child.Id) exited $($child.ExitCode). See logs in $work."
    }
}

if ($Build) {
    $buildLog = Join-Path $work 'build.log'
    Invoke-OwnedProcess $Unity @('-batchmode', '-nographics', '-quit', '-buildTarget', 'Win64',
        '-projectPath', ('"' + $project + '"'), '-executeMethod', 'WorldLifecycleBuild.BuildWindows',
        '-logFile', ('"' + $buildLog + '"')) 540
    if (!(Select-String -LiteralPath $buildLog -SimpleMatch 'WORLD_LIFECYCLE_BUILD_PASS' -Quiet)) {
        throw "Build completed without the success marker. See $buildLog."
    }
}

if ($Runs -eq 0) { return }
if (!(Test-Path -LiteralPath $player -PathType Leaf)) { throw 'Build the Windows player first with -Build.' }

$session = Join-Path $work ('runs-' + (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $session | Out-Null
for ($i = 1; $i -le $Runs; $i++) {
    $log = Join-Path $session ("run-$i.log")
    $report = Join-Path $session ("run-$i.json")
    $save = Join-Path $session ("save-$i.json")
    $arguments = @('-batchmode', '-screen-fullscreen', '0', '-screen-width', '1024', '-screen-height', '640',
        '-world-legacy', ('"' + $legacy + '"'), '-world-save', ('"' + $save + '"'),
        '-world-report', ('"' + $report + '"'), '-logFile', ('"' + $log + '"'))
    if ($NoGraphics) { $arguments += '-nographics' }

    Invoke-OwnedProcess $player $arguments 50
    $result = Get-Content -LiteralPath $report -Raw | ConvertFrom-Json
    if (!$result.passed) { throw "Probe did not pass. See $report." }
    Write-Output ('PASS pid={0} first={1:F2} ms (max gap {2:F2} ms) revisit={3:F2} ms (max gap {4:F2} ms)' -f
        $result.pid, $result.firstEntry.requestToSceneReadyMs, $result.firstEntry.largestUpdateGapMs,
        $result.revisit.requestToSceneReadyMs, $result.revisit.largestUpdateGapMs)
}
Write-Output "Reports: $session"
