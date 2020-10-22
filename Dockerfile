FROM buster:latest
ENTRYPOINT bash
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip python3-pillow
RUN pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
