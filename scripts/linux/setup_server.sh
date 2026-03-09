#!/bin/bash

# exit on command fail
set -e

# get the absolute path to where the script is located
declare -r SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# get the absolute path of project directory
declare -r PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# server environment directory
declare -r SERVER_ENV="$PROJECT_DIR/venv-server"

# server environment pip
declare -r SERVER_ENV_PIP="$SERVER_ENV/bin/pip3"

# server environment requirements
declare -r SERVER_REQUIREMENTS="$PROJECT_DIR/requirements/server.txt"

# ensure that the python environment exists
if [[ ! -d "$SERVER_ENV" ]]; then
    # create server virtual environment
    echo "Creating virtual environment"
    python3 -m venv "$SERVER_ENV"

else 
    echo "Virtual environment present"
fi

# ensure pip is latest version
echo "Upgrading pip"
"$SERVER_ENV_PIP" install --upgrade pip -q

# update environment with packages in requirements.txt
echo "Installing pip requirements"
"$SERVER_ENV_PIP" install -r "$SERVER_REQUIREMENTS" -q
