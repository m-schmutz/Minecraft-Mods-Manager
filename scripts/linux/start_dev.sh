#!/bin/bash

# exit on command fail
set -e

# get the absolute path to where the script is located
declare -r SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# get the absolute path of project directory
declare -r PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# server environment directory
declare -r SERVER_ENV_PY="$PROJECT_DIR/venv-server/bin/python3"

# start web server in debug mode
"$SERVER_ENV_PY" server.py