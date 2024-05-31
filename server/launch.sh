#!/bin/sh
# launch.sh

pwd
cd ~/emfcamp-2024
pwd

git pull

cd ./server
pwd

.venv/bin/pip install -r requirements.txt
.venv/bin/fastapi run main.py