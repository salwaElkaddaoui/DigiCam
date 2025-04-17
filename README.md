# Overview
Digit image classification on Raspberry Pi using TensorFlow Lite.
# Hardware and software setup
## Hardware
- a [raspberry pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
- a micro SD Card with a 16GB capacity. Read [this page](https://www.raspberrypi.org/documentation/installation/sd-cards.md) to know the minimum required size for the SD Card.

## Software
### I. Raspberry pi OS installation on the SD Card

#### Method 1: dd
Below I give a quick step-by-step guide, [here](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md) you'll find a more detailed description.
1. Download [the latest raspberry pi OS distribution](https://www.raspberrypi.org/downloads/raspberry-pi-os/) and unzip it: `unzip 2021-01-11-raspios-buster-armhf-lite.zip`
2. Insert the SD Card in your computer and look for its mount point in your file system using `lsblk -p`
4. Unmount it. For instance, in my case I run `umount /dev/sdX`, **/dev/sdX** being the mountpoint of my SD Card in my computer's file system.
5. Format it (I chose the ext4 file system, you could use fat32 too):
  ```bash
  sudo mkfs.ext4 /dev/sdX #adapt /dev/sdX to your case
  sudo fdisk /dev/sdX # this command creates a partition table.
  Press n to create a new partition.
  Choose the partition number (usually 1).
  Accept the default values for the first and last sectors to use the entire disk.
  Write the partition table and exit: Press w to write the changes to the disk and exit.
  ``` 
6. Copy the Raspbian OS image content to your SD Card: `sudo dd bs=4M if=2021-01-11-raspios-buster-armhf-lite.img of=/dev/mmcblk0 conv=fsync status=progress`
7. Insert the SD Card on you raspberry pi, and power the latter on.

#### Method 2: Startup Disk Creator
**Startup Disk Creator** is installed by default on ubuntu, I successfully tried it on Ubuntu 18.04.

#### Method 3: rpi-imager
This is the easiest method of all. You don't even need to download the .img file of the operating system in your computer.


- To communicate with the raspberry pi, you can either setup an **ssh connection**, or just **connect a monitor, a mouse and a keyboard to the raspberry pi** and use it as a regular computer (which I did).

### II. The establishment of an ssh connection in the raspberry pi (Headless mode)
The headless mode of the raspberry pi refers to operating the raspberry pi without any keyboard, monitor or mouse and instead controlling it using a network-based interface.
1. enable ssh in the raspberry pi:
```bash
sudo touch /media/$USER/bootfs/ssh
```
2. assign a static ip address to the ethernet interface of the raspberry pi:
```bash
sudo nano rootfs/etc/network/interfaces
auto eth0
iface eth0 inet static
    address 192.168.2.11
    netmask 255.255.255.0
    dns-nameservers 8.8.8.8 8.8.4.4
```
3. Set the username and the password for the raspberry pi: in the boot partition of the SD card create a file named userconf
```bash
cd /media/$USER/bootfs
sudo nano userconf
pi:<encrypted-password>
```
To encrypt the password, run this command in the terminal.
```bash
echo 'yourpassword' | openssl passwd -6 -stdin
```
4. On the side of the desktop machine, assign a static ip address to the ethernet interface:
```bash
sudo nano /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.2.12/24
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```
```bash
sudo netplan apply #so that the changes take effect
```
Note that there is no need for a gateway when cofiguring the ethernet interfaces of the raspberry pi and the host machine. The gateway is only necessary if one of the devices needs to access another network (e.g., the internet) through that interface. If you need to set a gateway for the Ethernet local network between the Raspberry Pi and the host machine, make sure the gateway's IP address is different from that of the Wi-Fi network to avoid conflicts between the two gateways.

5. insert the SD card into the raspberry pi, connect the ethernet ports of the raspberry pi and the desktop machine using an ethernet cable and power the raspberry pi on.

6. open a terminal in the desktop machine and establish an ssh connection:
```bash
ssh pi@192.168.1.11
```

7. Once logged in the raspberry pi, connect the raspberry pi to the internet using ```sudo raspi-config```. No need for a wifi dongle or any other hardware, the raspberry pi contains built-in hardware for wifi and bluetooth connectivity.

### III. Swap size extension to 2G
- ```sudo nano /etc/dphys-swapfile```
- Find the line that starts with CONF_SWAPSIZE and change it to this: ```CONF_SWAPSIZE=2048```
- Save te file and exit
- So that the changes take effect: ```sudo systemctl restart dphys-swapfile```
- Verify the new swapsize: ```free -h```

### IV. Docker installation on the Raspberry pi OS
1. Install **docker.io** instead of **docker-ce**: `sudo apt-get install docker.io`.
2. Check the installation success with `sudo docker run hello-world`
3. To spare yourself the pain of typing sudo at each docker command, run `sudo usermod -aG docker <your_username>`

### V. Creation of a tensorflow lite docker image
#### First: creation of base image from buster (buster is the version name of the Raspberry pi OS)
I used the first method of [this guide](https://docs.docker.com/develop/develop-images/baseimages/) to create a docker image of buster.
In short, run these 2 commands from your working directory:

`$ sudo debootstrap buster buster > /dev/null`

`$ sudo tar -C buster -c . | docker import - buster`

You'll notice that a folder named buster was created in your working directory. It contains the filesystem of your docker image.
To be able to instantiate a container that you can execute in interactive mode, you need to create a new image by building this Dockerfile:
```
FROM buster:latest
ENTRYPOINT bash
```
#### Second: writing a Dockerfile with the tensorflow lite interpreter

Building Bazel and Tensorflow on the raspberry pi takes ages because it requires a lot of computational resources and memory, maybe these are available on the raspberry pi 3 and 4, but for the raspberry pi model 2 model B, it's just impossible. So I used **Tensorflow Lite** instead.

[Tensorflow lite](https://www.tensorflow.org/lite/guide) is a set of tools for making inferences on resource-constrained devices. The advantage is 2-fold: inferences are faster and the model binary is smaller in size.

Tensorflow Lite is used only for inference (model definition and training have still to be done in tensorflow), and it has 2 main components:

1. **The Tensorflow Lite Converter**: install it on your computer to convert the tensorflow model to a tensorflow lite model.

2. **The Tensorflow Lite Interpreter**: install it on the raspberry pi to be able to do inferences on the tensorflow lite model.
