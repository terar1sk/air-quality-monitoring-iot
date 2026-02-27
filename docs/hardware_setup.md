# Hardware Setup

## System Overview

The monitoring device is built using two separate hardware components:

1. Raspberry Pi Pico 2 WH — main microcontroller unit
2. Cytron Robo Pico Pro — expansion and development board

The Robo Pico Pro board provides easier access to GPIO pins, power management and peripheral connections.

---
## Main Microcontroller

### Raspberry Pi Pico 2 WH

The Raspberry Pi Pico 2 WH acts as the primary processing unit.

Responsibilities:

- sensor data acquisition
- communication control
- database telemetry transmission
- OLED visualization control
- RTC synchronization

Features:

- RP2350 microcontroller
- built-in Wi-Fi support
- GPIO interfaces
- MicroPython support

Programming environment:

MicroPython firmware.

---
## Expansion Board

### Cytron Robo Pico Pro

The Robo Pico Pro functions as a carrier and development board for the Raspberry Pi Pico.

Provides:

- simplified GPIO access
- Grove / Maker connector compatibility
- stable power supply
- easier peripheral integration

The Pico 2 WH module is mounted directly onto the Robo Pico Pro.

---
## Connected Components

### RTC Module — DS1302

Used for accurate timestamp generation independent
from network connectivity.

Connection example:

CLK → GP2  
DIO → GP3  
CS → GP12  

---
### OLED Display — SSD1107

128x128 OLED display connected via I2C interface.

Pins:

SDA → GP0  
SCL → GP1  

Address:

0x3C

Used for displaying:

- current time
- temperature
- humidity
- system status

---
### Environmental Sensor

DHT22 sensor is used for environmental monitoring.

Measured parameters:

- temperature
- humidity

Connection:

DATA → GP27

---
## Network Connectivity

Wi-Fi connectivity is provided by the Raspberry Pi Pico 2 WH.

The device connects to a local wireless network and sends
telemetry data to database servers.

Automatic reconnection is implemented in firmware.