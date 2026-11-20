@echo off
setlocal
if not defined ONESTEP_VCVARS64 set "ONESTEP_VCVARS64=C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
where cl >nul 2>&1
if errorlevel 1 (
    call "%ONESTEP_VCVARS64%"
    if errorlevel 1 exit /b 1
)
if not exist "%~dp0out" mkdir "%~dp0out" || exit /b 1
set "TEMP=%~dp0out"
set "TMP=%~dp0out"
cl /nologo /std:c++17 /EHsc /permissive- /utf-8 /W4 /WX /O2 /Fo"%~dp0out\tactics.obj" /Fe"%~dp0out\tactics.exe" "%~dp0main.cpp"
