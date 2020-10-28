"""
Functions for using a picam rev2.
Based on: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
"""
from time import sleep
try:
    from picamera import PiCamera
except:
    raise ImportError('You need to pip3 install picamera')

def capture(output: str, resolution: tuple, fps: int) -> None:
    """Capture an image and save it.
        #Arguments:
            output: path where to save captures image, for instance: /home/pi/image.jpg
            resolution: image resolution, for example (640, 480)
            fps: frame rate, for example: 15
        #Returns:
            None
    """
    assert isinstance(output, str), "output should be a sting representing the path to output image "
    assert isinstance(fps, int), "fps should be an integer"
    assert isinstance(resolution, tuple), "resolution should be a tuple"

    camera = PiCamera()
    camera.resolution = tuple(resolution) #(640, 480)
    camera.framerate = fps #15
    camera.start_preview()
    sleep(0.1)
    camera.capture(args.out) #'/home/pi/image.jpg'
    camera.stop_preview()
