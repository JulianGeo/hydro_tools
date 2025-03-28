Fragmento de código

@echo off
set REPO_URL="https://github.com/JulianGeo/hydro_tools.git"
set REPO_NAME="hydro_tools"
set EXCEL_PROMPT="Please enter the full path to your Excel data file: "
set TARGET_BRANCH="develop"

REM Navigate to the directory where the BAT file is located
cd /d %~dp0

if not exist "%REPO_NAME%" (
    echo Cloning repository...
    git clone %REPO_URL%

    cd %REPO_NAME%
    git checkout %TARGET_BRANCH%
    if errorlevel 1 (
        echo Error: Could not checkout branch "%TARGET_BRANCH%". Please ensure it exists.
        goto end
    )
    
    echo Creating virtual environment...
    python -m venv venv
    echo Activating virtual environment...
    call venv\Scripts\activate
    echo Installing dependencies...
    REM pip install -r setup\requirements.txt
    python setup\setup.py
    echo.
) else (
    echo Repository already exists. Updating...
    cd %REPO_NAME%
    git checkout %TARGET_BRANCH%
    if errorlevel 1 (
        echo Error: Could not checkout branch "%TARGET_BRANCH%". Please ensure it exists.
        goto end
    )
    git pull origin %TARGET_BRANCH%
    call venv\Scripts\activate
    echo Ensuring dependencies are up-to-date...
    pip install -r setup\requirements.txt --upgrade
)

echo.
set /p EXCEL_PATH=%EXCEL_PROMPT%
echo.

python DiagramasStiff.py "%EXCEL_PATH%"

echo.
echo Plot generation complete! Press any key to exit...
pause