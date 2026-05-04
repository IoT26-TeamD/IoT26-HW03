from gpiozero import Button, MotionSensor
from picamera2 import Picamera2
from libcamera import Transform
from time import sleep
from signal import pause
import sys
import os

button = Button(2)
pir = MotionSensor(17)
picam2 = Picamera2(camera_num=0)

config = picam2.create_still_configuration(
    main={"size": (1920, 1080)},
    transform=Transform(hflip=True, vflip=True) 
)
picam2.configure(config)

picam2.start()
print("Cam activated")

i = 0
save_path = '/home/IoT26/'
if not os.path.exists(save_path):
    print(f"경고: {save_path} 폴더가 없어 현재 폴더에 저장합니다.")
    save_path = './'

def stop_camera():
    print("\nButton pressed, halt")
    picam2.stop()
    sys.exit()

def take_photo():
    global i
    i += 1
    
    filename = f'{save_path}image_{i}.jpg'
    picam2.capture_file(filename)
    
    print(f'picture is on : {filename}')
    
    # 10초 동안 대기 (중복 촬영 방지)
    sleep(10)

button.when_pressed = stop_camera
pir.when_motion = take_photo

try:
    pause()
except KeyboardInterrupt:
    stop_camera()
