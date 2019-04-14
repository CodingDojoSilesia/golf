#!/bin/bash
set -e
python3 install.py
mkdir /sys/fs/cgroup/cpu/NSJAIL
mkdir /sys/fs/cgroup/memory/NSJAIL
mkdir /sys/fs/cgroup/pids/NSJAIL
export FLASK_DEBUG=1
export FLASK_APP=app.py
python3 -m flask run --host=0.0.0.0 --port=5000
