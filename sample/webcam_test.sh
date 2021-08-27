#!/usr/bin/env bash
echo "=====[ Logitech Webcam Test ]=====" #로지텍 C310 기준 웹캠 테스트를 위한 스크립트
echo "=====[ 1. usb connected check ]=====" #연결되어있는 usb장치를 확인합니다. logitech webcam이 있다면 정상
lsusb
echo " "

echo "=====[ 2. installing packages ]=====" #테스트를 위하여 v4l2-ctl & fswebcam 패키지를 설치합니다.
sudo apt-get install v4l2-ctl
sudo apt-get install fswebcam
echo " "

echo "=====[ 3. webcam spec. ]=====" #웹캠의 간단한 spec을 화면에 표출합니다.
v4l2-ctl -V
echo " "

echo "=====[ 4. fswebcam test ]=====" #웹캠으로 사진을 한번찍어 현재 폴더에 testimg.jpg 로 저장합니다.
fswebcam -r 1280*960 --no-banner testimg.jpg
echo " "

echo "=====[ Done ]====="

