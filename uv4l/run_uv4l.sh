#!/usr/bin/env bash
echo "=====[ UV4L Starting Script ]====="
echo "=====[ 1. usb connected check ]=====" #연결되어있는 usb장치를 확인합니다. logitech webcam이 있다면 정상
lsusb
echo " "

echo "=====[ 2. webcam spec. ]=====" #웹캠의 간단한 spec을 화면에 표출합니다.
v4l2-ctl -V
echo " "

echo "=====[ 3. run uv4l. ]=====" #UV4L 스트리밍을 시작합니다.
/usr/bin/uv4l -k --sched-rr --mem-lock --config-file=/etc/uv4l/uv4l-uvc.conf --driver uvc --driver-config-file=/etc/uv4l/uv4l-uvc.conf --server-option=--editable-config-file=/etc/uv4l/uv4l-uvc.conf --device-id 046d:081b
echo " "

echo "=====[ Done ]====="
