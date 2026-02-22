#!/bin/bash

# exit on command fail
set -e

# server python environment directory
declare -r ENV="venv-server"

# change to server directory (directory where this script is located)
cd "$(dirname "${BASH_SOURCE[0]}")"

# ensure that the python environment exists
if [[ ! -d "$ENV" ]]; then
    # create server virtual environment
    echo "Creating virtual environment"
    python3 -m venv "$ENV"

else 
    echo "Virtual environment present"
fi

# activate virtual environment
source ./$ENV/bin/activate

# ensure pip is latest version
echo "Upgrading pip"
pip3 install --upgrade pip -q

# update environment with packages in requirements.txt
echo "Installing pip requirements"
pip3 install -r requirements.txt -q
