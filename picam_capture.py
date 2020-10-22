from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.start_preview()
sleep(0.1)
camera.capture('/home/pi/image.jpg')
camera.stop_preview()
