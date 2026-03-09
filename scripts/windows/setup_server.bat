@echo off

rem get the absolute path to where the script is located
pushd "%~dp0"
set "SCRIPT_DIR=%CD%"
popd

rem get the absolute path of project directory
pushd "%SCRIPT_DIR%\..\.."
set "PROJECT_DIR=%CD%"
popd

rem server environment directory
set "SERVER_ENV=%PROJECT_DIR%\venv-server"

rem server environment pip
set "SERVER_ENV_PY=%SERVER_ENV%\Scripts\python.exe"

rem server environment requirements
set "SERVER_REQUIREMENTS=%PROJECT_DIR%\requirements\server.txt"

rem ensure that the python environment exists
if exist "%SERVER_ENV%\" (
    echo Virtual environment present
) else (
    rem create server virtual environment
    echo Creating virtual environment
    python3.exe -m venv "%SERVER_ENV%"
)

rem ensure pip is latest version
echo Upgrading pip
"%SERVER_ENV_PY%" -m pip install --upgrade pip -q

rem update environment with packages in requirements.txt
echo Installing pip requirements
"%SERVER_ENV_PY%" -m pip install -r "%SERVER_REQUIREMENTS%" -q
