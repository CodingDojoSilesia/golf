#!/bin/bash
uwsgi --http 0.0.0.0:5000 --master --module app:app --processes 4
