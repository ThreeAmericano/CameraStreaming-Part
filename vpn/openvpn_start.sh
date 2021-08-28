#!/usr/bin/env bash
echo "===[ Start OpenVPN ]==="
sudo openvpn --config ./camera.ovpn
sleep 1
echo " "

echo "===[ Check VPN Status ]==="
systemctl status openvpn | grep Active
echo " "


