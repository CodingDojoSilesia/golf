#!/bin/bash
iptables -A OUTPUT -p all -m owner --uid-owner socek -j DROP
uwsgi --http 0.0.0.0:5000 --master --module app:app --processes 4
