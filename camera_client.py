#####################################################
#
# Camera Client Program
# 2021-08-27
#
#####################################################
from module import rabbitmq_clinet as rbc
import RPi.GPIO as GPIO
import time
import json
import threading

FLAG_RUN_LIGHT = False
PIN_LIGHT = 2
PIN_LUX = 3

print("[init] GPIO Table")
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LIGHT, GPIO.OUT)
GPIO.setup(PIN_LUX, GPIO.IN)


# AMQP 메세지 콜백함수 지정
def callback(ch, method, properties, body):
    global FLAG_RUN_LIGHT

    # AMQP 메세지 수신
    print(method.delivery_tag)
    print(" [x] Received %r" % body.decode())

    # JSON형식으로 메세지 정제
    try:
        body_decode = body.decode()
        json_data = json.loads(body_decode)
    except Exception as e:
        print("not json data")
        return False

    # 올바른 JSON 메세지인지 확인 (현재 제어메세지가 한개임 camera제어부분만 잇음)
    light_onoff_sign = 'none'
    try:
        temp = json_data['Producer']
        temp = json_data['command']
        light_onoff_sign = json_data['sign']
    except Exception as e:
        print("not good json form")
        return False
    print(light_onoff_sign)

    # 얼굴인식 진행/종료 신호에 따른 동작
    if light_onoff_sign == "start":
        FLAG_RUN_LIGHT = True
    elif light_onoff_sign == "end":
        FLAG_RUN_LIGHT = False
    else:
        pass


def gpio_control():
    global FLAG_RUN_LIGHT
    while True:
        if FLAG_RUN_LIGHT:
            # 얼굴인식 진행/종료 신호에 따른 동작
            try:
                lux_signal = GPIO.input(PIN_LUX)
                print("LUX SIGN : %r" % lux_signal)
                if lux_signal:
                    GPIO.output(PIN_LIGHT, GPIO.HIGH)
                else:
                    GPIO.output(PIN_LIGHT, GPIO.LOW)
                    time.sleep(0.2)	
            except Exception as e:
                print("gpio error!! %r" % e)


# GPIO control Thread 실행
t = threading.Thread(target=gpio_control, daemon=True)
t.start()
time.sleep(0.5)

# RabbitMQ 연결
print("[init] RabbitMQ Connection")
rb = rbc.RabbitmqClient('211.179.42.130', 5672, 'rabbit', 'MQ321')
conn = rb.connect_server()

camera_channel = rbc.RabbitmqChannel(conn)
camera_channel.open_channel()
camera_channel.publish_exchange('webos.topic', 'webos.test.info', '{nice}')
camera_channel.consume_setting('webos.camera', callback)

print("[start] RabbitMQ Consume")
try:
    camera_channel.consume_starting()
except KeyboardInterrupt:
    print("KEY BOARD INTERRUPT!!")
    rb.disconnect_server()
    GPIO.cleanup()

