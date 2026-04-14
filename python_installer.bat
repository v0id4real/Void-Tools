@echo off
setlocal enabledelayedexpansion
title Void-Tools Setup
color 0c

echo.
echo  ^<^<^< VOID-TOOLS SETUP ^>^>^>
echo  ================================
echo.

:: ------------------------------------------------
::  1. Kill active Python processes
:: ------------------------------------------------
echo  [1/6] ^> Killing Python processes...
taskkill /f /im python.exe >nul 2>nul
taskkill /f /im pythonw.exe >nul 2>nul
taskkill /f /im pip.exe >nul 2>nul
timeout /t 1 /nobreak >nul
echo        Done.

:: ------------------------------------------------
::  2. Wipe all pip packages
:: ------------------------------------------------
echo  [2/6] ^> Wiping pip packages...
python -m pip freeze > "%TEMP%\pip_list.txt" 2>nul
python -m pip uninstall -y -r "%TEMP%\pip_list.txt" >nul 2>nul
del "%TEMP%\pip_list.txt" >nul 2>nul
echo        Done.

:: ------------------------------------------------
::  3. Uninstall Python (registry + MSI)
:: ------------------------------------------------
echo  [3/6] ^> Uninstalling Python...
for /f "tokens=*" %%K in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall" 2^>nul') do (
    for /f "tokens=2*" %%A in ('reg query "%%K" /v "DisplayName" 2^>nul ^| findstr /i "Python"') do (
        for /f "tokens=2*" %%C in ('reg query "%%K" /v "UninstallString" 2^>nul') do (
            start /wait "" cmd /c "%%D /quiet /norestart" >nul 2>nul
        )
    )
)
for /f "delims=" %%I in ('wmic product where "Name like ''Python%%''" get IdentifyingNumber /format:value 2^>nul ^| findstr "IdentifyingNumber"') do (
    set "LINE=%%I"
    set "GUID=!LINE:IdentifyingNumber=!"
    set "GUID=!GUID:~1!"
    msiexec /x !GUID! /quiet /norestart >nul 2>nul
)
echo        Done.

:: ------------------------------------------------
::  4. Delete leftover folders
:: ------------------------------------------------
echo  [4/6] ^> Removing leftover folders...
for %%D in (
    "%LOCALAPPDATA%\Programs\Python"
    "%APPDATA%\Python"
    "%LOCALAPPDATA%\pip"
) do (
    if exist "%%~D" (
        takeown /f "%%~D" /r /d y >nul 2>nul
        icacls "%%~D" /grant "%USERNAME%":F /t >nul 2>nul
        rd /s /q "%%~D" >nul 2>nul
    )
)
echo        Done.

:: ------------------------------------------------
::  5. Clean registry + user PATH
:: ------------------------------------------------
echo  [5/6] ^> Cleaning registry and PATH...
reg delete "HKCU\Software\Python" /f >nul 2>nul
powershell -NoProfile -NonInteractive -Command "$u=[System.Environment]::GetEnvironmentVariable('PATH','User'); $c=($u -split ';' | Where-Object {$_ -notmatch '(?i)python' -and $_ -notmatch '(?i)Scripts' -and $_ -ne ''} | Select-Object -Unique) -join ';'; [System.Environment]::SetEnvironmentVariable('PATH',$c,'User');" >nul 2>nul
echo        Done.

echo.
echo  ================================
echo   Cleanup complete. Setting up...
echo  ================================
echo.

:: ------------------------------------------------
::  6. Refresh PATH + locate Python
:: ------------------------------------------------
for /f "skip=2 tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USERPATH=%%B"
if defined USERPATH set "PATH=%USERPATH%;%PATH%"

set "PY=python"
where python >nul 2>nul
if errorlevel 1 (
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%D\python.exe" set "PY=%%D\python.exe"
    )
)

:: Check Python, install if missing
"%PY%" --version >nul 2>&1
if errorlevel 1 goto :install_python
goto :python_ready

:install_python
echo  [6/6] ^> Python not found, downloading...
curl -L "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe" -o "%APPDATA%\py_setup.exe"
if not exist "%APPDATA%\py_setup.exe" (
    echo.
    echo  [!] Download failed. Check your connection.
    pause & exit /b 1
)
echo        Installing Python 3.11.5...
start /wait "" "%APPDATA%\py_setup.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0 Include_launcher=1
del "%APPDATA%\py_setup.exe" >nul 2>nul
for /f "skip=2 tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USERPATH=%%B"
if defined USERPATH set "PATH=%USERPATH%;%PATH%"
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" set "PY=%%D\python.exe"
)
echo        Python 3.11.5 installed.

:python_ready
echo  [6/6] ^> Python detected:
"%PY%" --version

echo.
echo        Checking modules...
"%PY%" -c "import sys, os, time, random, string, json, threading, itertools, shutil, re, queue, webbrowser, concurrent.futures" >nul 2>&1
if errorlevel 1 (
    echo  [!] Missing stdlib module. Reinstall Python.
    pause & exit /b 1
)

"%PY%" -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo        Installing requests...
    "%PY%" -m pip install requests --quiet
)

echo        All modules OK.
