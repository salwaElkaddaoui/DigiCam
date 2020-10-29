"""
Functions for using a picam rev2.
Based on: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera
"""
from time import sleep
try:
    from picamera import PiCamera
except:
    raise ImportError('You need to pip3 install picamera')

def capture(resolution: tuple, fps: int) -> None:
    """Capture an image and return it as a numpy array.
        #Arguments:
            resolution: image resolution, for example (640, 480)
            fps: frame rate, for example: 15
        #Returns:
            image as numpy array
    """
    assert isinstance(fps, int), "fps should be an integer"
    assert isinstance(resolution, tuple), "resolution should be a tuple"

    output = np.empty((resolution[0], resolution[1], 3), dtype=np.uint8)
    camera = PiCamera()
    camera.resolution = tuple(resolution) #(640, 480)
    camera.framerate = fps #15
    camera.start_preview()
    sleep(0.1)
    camera.capture(output, 'rgb')
    camera.stop_preview()
    return output
    # camera.capture(args.out) #'/home/pi/image.jpg'
