param(
    [Parameter(Mandatory=$true)][string]$Method,
    [string]$Report='checks.json',
    [string]$Log='editor.log',
    [switch]$Graphics,
    [switch]$InjectError
)
$ErrorActionPreference='Stop'
$labPath=$PSScriptRoot
$editorPath='C:/Program Files/Unity/Hub/Editor/6000.0.77f1/Editor/Unity.exe'
$logPath=Join-Path $labPath "Logs/$Log"
New-Item -ItemType Directory -Path (Split-Path $logPath) -Force | Out-Null
$arguments=@('-batchmode','-projectPath',$labPath,'-executeMethod',$Method,'-labReport',$Report,'-logFile',$logPath)
if (-not $Graphics) { $arguments+= '-nographics' }
if ($Method -eq 'LabBatch.Play') { $arguments+= '-labRun' }
if ($InjectError) { $arguments+= '-labInjectError' }
$engine=Start-Process -FilePath $editorPath -ArgumentList $arguments -WindowStyle Hidden -PassThru
$limit=(Get-Date).AddMinutes(10)
while (-not $engine.WaitForExit(1000)) {
    if ((Get-Date) -gt $limit) { $engine.Kill(); throw 'Owned Unity run exceeded ten minutes' }
}
$engine.Refresh()
Write-Output ('Unity exit code: '+$engine.ExitCode)
exit $engine.ExitCode
