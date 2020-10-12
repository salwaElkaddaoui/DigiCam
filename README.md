# Hardware and software setup
## Hardware
- a [raspberry pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
- a micro SD Card with a 16GB capacity. Read [here](https://www.raspberrypi.org/documentation/installation/sd-cards.md) to know the minimum required size for the SD Card.

## Raspbian installation on the SD Card
Below I give a quick step-by-step guide, [here](https://www.raspberrypi.org/documentation/installation/installing-images/) you'll find a more detailed description.
1. Download [the latest raspbian distribution](https://www.raspberrypi.org/downloads/raspberry-pi-os/) and unzip it like this: `unzip 2020-08-20-raspios-buster-armhf.zip`
2. Install **rpi-manager** on your computer: `sudo apt-get install rpi-manager`
3. Insert the SD Card in your computer and look for its mount point in your file system using `lsblk -p`
4. Unmount it. For instance, in my case I run `umount /dev/mmcblk0`, **/dev/mmcblk0** being the mountpoint of my SD Card in my computer's file system.
5. Copy the Raspbian OS image content to your SD Card: `dd bs=4M if=2020-08-20-raspios-buster-armhf.img of=/dev/mmcblk0 conv=fsync`
6. Insert the SD Card on you raspberry pi.

## Dependencies installation on raspbian
You can either setup an **ssh connection** to the raspberry pi, or just **connect a monitor, a mouse and a keyboard to the raspberry pi** and use it as a regular computer (which I did).
- For those of you who, like me, struggle with the english layout of the keyboard, you can change it to the french layout with `setxkbmap fr`

### Docker installation
1. Install **docker.io** instead of **docker-ce**: `sudo apt-get install docker.io`
I don't know why, but the package manager on raspbian is unable to locate docker-ce.
2. Check the installation success with `sudo docker run hello-world`.
