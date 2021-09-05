#!/usr/bin/env bash
sudo ./vpn/openvpn_start.sh
./uv4l/run_uv4l.sh
python3 ./camera_client.py

