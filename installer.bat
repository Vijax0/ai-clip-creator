@echo off
setlocal

echo Installing application...
set "INSTALL_DIR=%~dp0miniconda"

if not exist "%INSTALL_DIR%" (
    echo Downloading Miniconda...
    curl -o "miniconda_installer.exe" "https://repo.anaconda.com/miniconda/Miniconda3-py39_25.7.0-2-Windows-x86_64.exe"

    echo Installing Miniconda...
    start /wait "" "miniconda_installer.exe" /S /RegisterPython=0 /AddToPath=0 /InstallationType=JustMe /D=%INSTALL_DIR%
    del "miniconda_installer.exe"
)

echo Creating conda environment...
call "%INSTALL_DIR%\Scripts\activate.bat"

if not exist "%INSTALL_DIR%\envs\app_env" (
    echo Creating python environment...
    call conda create -y -n app_env python=3.11 -q
)

call conda activate app_env
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate app_env environment
    echo Installation aborted to prevent system Python modification
    pause 
    exit /b 1
)

echo Installing PyTorch...
call conda install pytorch==2.5.1 -c pytorch -c nvidia -y
if %ERRORLEVEL% GTR 1 (
    echo ERROR: PyTorch installation failed with error code %ERRORLEVEL%!
    pause
    exit /b %ERRORLEVEL%
)

echo Installing additional requirements...
call pip install -r requirements.txt

echo Installation complete!
pause