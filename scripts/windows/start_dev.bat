@echo off

rem get the absolute path to where the script is located
pushd "%~dp0"
set "SCRIPT_DIR=%CD%"
popd

rem get the absolute path of project directory
pushd "%SCRIPT_DIR%\..\.."
set "PROJECT_DIR=%CD%"
popd

rem server environment pip
set "SERVER_ENV_PY=%PROJECT_DIR%\venv-server\Scripts\python.exe"

rem run the server in dev mode
"%SERVER_ENV_PY%" server.py