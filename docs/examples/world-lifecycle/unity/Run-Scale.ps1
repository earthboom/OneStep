[CmdletBinding()]
param(
    [switch]$Build,
    [switch]$Smoke,
    [ValidateRange(1, 4)][int]$Rounds = 4,
    [string]$Unity = 'C:\Program Files\Unity\Hub\Editor\6000.0.77f1\Editor\Unity.exe'
)

$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
if ($Build) { & (Join-Path $project 'Run-Probe.ps1') -Build -Runs 0 -Unity $Unity }
$player = Join-Path $project 'Build/WorldLifecycle.exe'
if (!(Test-Path -LiteralPath $player -PathType Leaf)) { throw 'Build the Windows Player first with -Build.' }

$session = Join-Path $project ('Work/scale-' + (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $session | Out-Null

# Balanced four-condition order. Each mode occupies each run position once.
$orders = @(
    @('resident-full', 'stream-full', 'stream-coarse', 'resident-coarse'),
    @('stream-full', 'resident-coarse', 'resident-full', 'stream-coarse'),
    @('resident-coarse', 'stream-coarse', 'stream-full', 'resident-full'),
    @('stream-coarse', 'resident-full', 'resident-coarse', 'stream-full')
)
if ($Smoke) { $Rounds = 1 }
for ($round = 1; $round -le $Rounds; $round++) {
    $version = if ($round % 2) { 1 } else { 2 }
    $fixture = (Resolve-Path (Join-Path $project "../fixtures/legacy-v$version.json")).Path
    $original = (Get-FileHash -LiteralPath $fixture).Hash
    $order = if ($Smoke) { @('stream-coarse') } else { $orders[$round - 1] }
    foreach ($mode in $order) {
        $stem = Join-Path $session "$round-$mode"
        $arguments = @('-force-d3d11', '-screen-fullscreen', '0', '-screen-width', '1280', '-screen-height', '720',
            '-world-scale', $mode, '-world-scale-fixture', $version,
            '-world-legacy', ('"' + $fixture + '"'), '-world-save', ('"' + $stem + '.save.json"'),
            '-world-scale-report', ('"' + $stem + '.json"'), '-logFile', ('"' + $stem + '.log"'))
        $child = Start-Process -FilePath $player -ArgumentList $arguments -WorkingDirectory $project -WindowStyle Hidden -PassThru
        if (!$child.WaitForExit(105000)) {
            Stop-Process -Id $child.Id -Force -ErrorAction SilentlyContinue
            throw "Player $($child.Id) exceeded 105 seconds. See $stem.log."
        }
        if ($child.ExitCode -ne 0) { throw "Player $($child.Id) exited $($child.ExitCode). See $stem.log." }
        $result = Get-Content -LiteralPath ($stem + '.json') -Raw | ConvertFrom-Json
        if (!$result.passed -or $result.pid -ne $child.Id -or $result.mode -ne $mode -or $result.fixtureVersion -ne $version) {
            throw "Player report failed verification. See $stem.json."
        }
        if ((Get-FileHash -LiteralPath $fixture).Hash -ne $original) { throw "Source fixture $fixture changed." }
        Write-Output "PASS round=$round mode=$mode fixture=v$version pid=$($result.pid) frames=$($result.frameSamples.Count) npcUpdates=$($result.npcUpdates)"
    }
}
Write-Output "Reports: $session"
