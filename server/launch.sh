#!/bin/sh
# launch.sh

cd ~/emfcamp-2024

git pull

cd ./server

.venv/bin/pip install -r requirements.txt
.venv/bin/fastapi run main.py