param(
    [ValidatePattern('^[A-Za-z0-9_-]+$')][string]$Session='player-run-1',
    [switch]$Interactive
)
$ErrorActionPreference='Stop'
$labRoot=$PSScriptRoot
$player=Join-Path $labRoot 'Build/TechniqueLab.exe'
if (-not (Test-Path -LiteralPath $player)) {throw 'Build the Unity player first'}
$log=Join-Path $labRoot "Logs/$Session.log"
New-Item -ItemType Directory -Path (Split-Path $log) -Force | Out-Null
$arguments=@('-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-force-d3d11','-logFile',$log,'-labReport',"$Session.json")
if (-not $Interactive) {$arguments+=@('-batchmode','-labRun')}
$started=[DateTime]::UtcNow
$windowStyle=if($Interactive){'Normal'}else{'Hidden'}
$engine=Start-Process -FilePath $player -ArgumentList $arguments -WindowStyle $windowStyle -PassThru
$limit=(Get-Date).AddMinutes(10)
while (-not $engine.WaitForExit(1000)) {
    if ((Get-Date) -gt $limit) {$engine.Kill();throw 'Owned player run exceeded ten minutes'}
}
$engine.Refresh()
$sourceFiles=Get-ChildItem -LiteralPath (Join-Path $labRoot 'Assets') -Recurse -Filter '*.cs'
$identities=@{}
foreach($source in $sourceFiles){$identities[$source.FullName.Substring($labRoot.Length+1)]=(Get-FileHash -LiteralPath $source.FullName -Algorithm SHA256).Hash}
$record=@{utcStart=$started.ToString('o');utcEnd=[DateTime]::UtcNow.ToString('o');exitCode=$engine.ExitCode;session=$Session;
    playerSha256=(Get-FileHash -LiteralPath $player -Algorithm SHA256).Hash;sourceSha256=$identities;interactive=[bool]$Interactive}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $labRoot "Results/$Session-process.json") -Encoding utf8
Write-Output ('Player exit code: '+$engine.ExitCode)
exit $engine.ExitCode
