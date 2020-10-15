# Hardware and software setup
## Hardware
- a [raspberry pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
- a micro SD Card with a 16GB capacity. Read [here](https://www.raspberrypi.org/documentation/installation/sd-cards.md) to know the minimum required size for the SD Card.

## Software
### Raspberry pi OS installation on the SD Card
Below I give a quick step-by-step guide, [here](https://www.raspberrypi.org/documentation/installation/installing-images/) you'll find a more detailed description.
1. Download [the latest raspbian distribution](https://www.raspberrypi.org/downloads/raspberry-pi-os/) and unzip it like this: `unzip 2020-08-20-raspios-buster-armhf.zip`
2. Insert the SD Card in your computer and look for its mount point in your file system using `lsblk -p`
3. Unmount it. For instance, in my case I run `umount /dev/mmcblk0`, **/dev/mmcblk0** being the mountpoint of my SD Card in my computer's file system.
4. Copy the Raspbian OS image content to your SD Card: `dd bs=4M if=2020-08-20-raspios-buster-armhf.img of=/dev/mmcblk0 conv=fsync status=progress`
5. Insert the SD Card on you raspberry pi, and power the latter on.

- To communicate with the raspberry pi, you can either setup an **ssh connection**, or just **connect a monitor, a mouse and a keyboard to the raspberry pi** and use it as a regular computer (which I did).
- For those of you who, like me, struggle with the english layout of the keyboard, you can change it to the french layout with `setxkbmap fr`

### Docker installation on the Raspberry OS
1. Install **docker.io** instead of **docker-ce**: `sudo apt-get install docker.io`.
2. Check the installation success with `sudo docker run hello-world`

### Creation of a tensorflow docker image
#### First: creation of base image from buster (buster is the version name of the raspberry pi OS)
I used the first method of [this guide](https://docs.docker.com/develop/develop-images/baseimages/) to create a docker image of buster.
In short, run these 2 commands from your working directory:

`$ sudo debootstrap buster buster > /dev/null`

`$ sudo tar -C buster -c . | docker import - buster`

You'll notice that a folder named buster was created in your working directory. It contains the filesystem of your docker image.
The to be able to instantiate a container that you can execute in the interactive mode, you need to create a new image by building this Dockerfile:
```
FROM buster:latest
ENTRYPOINT bash
```
#### Second: writing of the tensorflow Dockerfile
The following steps are:
- installation of openjdk-8-jdk
- installation of bazel
- building tensorflow using a script in tensorflow/tools/ci_build/build_raspberrypi.sh
