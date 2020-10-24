"""
Capture an image with a picam rev2.
Based on: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
"""
try
    from picamera import PiCamera
except:
    raise ImportError('You need to pip3 install picamera')
from time import sleep
import argparse, os


if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--resolution', dest='res', help='image path')
    parser.add_argument('--fps', dest='fps', type=int, help='model path')
    parser.add_argument('--output', dest='out', help='model path')
    args = parser.parse_args()

    if not os.path.exists(args.out):
        raise ValueError('Given output path does not exist.')

    camera = PiCamera()
    camera.resolution = tuple(args.res) #(640, 480)
    camera.framerate = args.fps #15
    camera.start_preview()
    sleep(0.1)
    camera.capture(args.out) #'/home/pi/image.jpg'
    camera.stop_preview()
