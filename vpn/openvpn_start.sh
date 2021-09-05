#!/usr/bin/env bash
echo "===[ Start OpenVPN ]==="
#sudo openvpn --config ./camera.ovpn --askpass auth.txt
sudo openvpn --config /home/pi/camera_client/vpn/camera.ovpn --askpass /home/pi/camera_client/vpn/auth.txt
sleep 1
echo " "

echo "===[ Check VPN Status ]==="
systemctl status openvpn | grep Active
echo " "
sleep 100

