# lights
Raspberry pi zero light controller to work with Home Assistant

# Requirements
Refer to this document about how to install adafruit software and enable I2C and SPI
[installing circuitpython on raspi]: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

Install libatlas to be able to import numpy
```bash
sudo apt-get install libatlas-base-dev
```
Then install requirements with sudo
```bash
sudo pip3 install -r requirements.txt
```
Run with sudo
```bash
sudo python3 run.py
```