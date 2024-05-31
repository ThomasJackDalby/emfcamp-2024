#!/bin/sh
# launch.sh

cd /home/fish/emfcamp-2024
git reset --hard
git pull
cd ./server
chmod 755 launch.sh
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --log-config /home/fish/emfcamp-2024/server/log.ini