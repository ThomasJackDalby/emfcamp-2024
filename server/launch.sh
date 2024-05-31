#!/bin/sh
# launch.sh

# navigate to the project directory
cd /home/dalbypi/repos/emfcamp-2024

# pull any updates
git pull

# install python requirements
.venv/bin/pip install -r requirements.txt

# run
.venv/bin/fastapi run main.py