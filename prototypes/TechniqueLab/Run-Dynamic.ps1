param(
    [ValidatePattern('^[A-Za-z0-9_-]+$')][string]$Session='dynamic-run-1',
    [ValidateSet(0,1)][int]$Order=0,
    [switch]$Visible,
    [switch]$Interactive
)
$ErrorActionPreference='Stop'
$labRoot=$PSScriptRoot
$player=Join-Path $labRoot 'DynamicBuild/DynamicLab.exe'
if(-not(Test-Path -LiteralPath $player)){throw 'Run DynamicBatch.Build first'}
$log=Join-Path $labRoot "Logs/$Session.log"
New-Item -ItemType Directory -Path (Split-Path $log) -Force | Out-Null
$arguments=@('-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-force-d3d11','-logFile',$log,'-labReport',"$Session.json",'-dynamicOrder',"$Order")
if(-not $Interactive){$arguments+='-dynamicRun'}
$started=[DateTime]::UtcNow
$style=if($Interactive -or $Visible){'Normal'}else{'Hidden'}
$engine=Start-Process -FilePath $player -ArgumentList $arguments -WindowStyle $style -PassThru
$limit=(Get-Date).AddMinutes(10)
while(-not $engine.WaitForExit(1000)){if((Get-Date)-gt $limit){$engine.Kill();throw 'Owned dynamic player exceeded ten minutes'}}
$engine.Refresh()
$identities=@{}
foreach($source in (Get-ChildItem -LiteralPath (Join-Path $labRoot 'Assets') -Recurse -Filter '*.cs'))
{$identities[$source.FullName.Substring($labRoot.Length+1)]=(Get-FileHash -LiteralPath $source.FullName -Algorithm SHA256).Hash}
$record=@{utcStart=$started.ToString('o');utcEnd=[DateTime]::UtcNow.ToString('o');exitCode=$engine.ExitCode;session=$Session;interactive=[bool]$Interactive;visible=[bool]($Interactive -or $Visible);order=$Order;
    playerSha256=(Get-FileHash -LiteralPath $player -Algorithm SHA256).Hash;
    managedAssemblySha256=(Get-FileHash -LiteralPath (Join-Path $labRoot 'DynamicBuild/DynamicLab_Data/Managed/Assembly-CSharp.dll') -Algorithm SHA256).Hash;
    sourceSha256=$identities}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $labRoot "Results/Dynamic/$Session-process.json") -Encoding utf8
Write-Output ('Dynamic player exit code: '+$engine.ExitCode)
exit $engine.ExitCode
