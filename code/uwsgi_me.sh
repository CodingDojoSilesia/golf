#!/bin/bash
mkdir /sys/fs/cgroup/cpu/NSJAIL
mkdir /sys/fs/cgroup/memory/NSJAIL
mkdir /sys/fs/cgroup/pids/NSJAIL
uwsgi --http 0.0.0.0:5000 --master --module app:app --processes 4
