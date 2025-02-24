#!/usr/bin/env sh
. .venv/bin/activate
nohup python bot.py > bot.log 2>&1 &
