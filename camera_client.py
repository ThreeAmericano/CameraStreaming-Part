#####################################################
#
# Camera Client Program
# 2021-09-05
#
#####################################################
from module import rabbitmq_clinet as rbc
import RPi.GPIO as GPIO
import time
import json
import threading

FLAG_RUN_LIGHT = False
LIGHT_TIME_LIMIT = 180
PIN_LIGHT = 2
PIN_LUX = 3

print("[init] GPIO Table")
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LIGHT, GPIO.OUT)
GPIO.setup(PIN_LUX, GPIO.IN)
time.sleep(0.1)
GPIO.output(PIN_LIGHT, GPIO.LOW)

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

    if json_data['Producer'] != 'server':
        print("not good Producer : %r" % json_data['Producer'])
        return False
    if json_data['command'] != 'facer_sign':
        print("not good command : %r" % json_data['command'])
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
    before_time = time.time()
    now_time = time.time() 

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
        else:
            before_time = time.time()
            GPIO.output(PIN_LIGHT, GPIO.LOW)

        # 제한시간 초과시 동작을 강제로 OFF (인터넷 연결이상 등 장애가 있는 것으로 판단)
        now_time = time.time()
        if (now_time - before_time) > LIGHT_TIME_LIMIT:
            FLAG_RUN_LIGHT = False


# GPIO control Thread 실행
t = threading.Thread(target=gpio_control, daemon=True)
t.start()
time.sleep(0.5)

# RabbitMQ 연결
print("[init] RabbitMQ Connection")
rb = rbc.RabbitmqClient('211.179.42.130', 5672, 'rabbit', 'MQ321')
conn = rb.connect_server()

camera_channel = rbc.RabbitmqChannel(conn)
time.sleep(0.5)
camera_channel.open_channel()
time.sleep(0.5)
camera_channel.publish_exchange('webos.topic', 'webos.test.info', '{nice}')
camera_channel.consume_setting('webos.camera', callback)

print("[start] RabbitMQ Consume")
try:
    camera_channel.consume_starting()
except KeyboardInterrupt:
    print("KEY BOARD INTERRUPT!!")
    rb.disconnect_server()
    GPIO.cleanup()

