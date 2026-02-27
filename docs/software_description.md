# Software Description

## Overview

The software component of the IoT Air Quality Monitoring System is developed using MicroPython and runs on the Raspberry Pi Pico 2 WH microcontroller.

The firmware is responsible for collecting environmental data, processing timestamps, displaying information locally and transmitting telemetry data to database servers.

---
## Firmware Architecture

The software is organized into several modules located inside the firmware directory.

Main responsibilities include:

- sensor data acquisition
- Wi-Fi communication
- timestamp generation
- OLED visualization
- database communication

---
## Main Application

### main.py

The main application controls the entire monitoring process.

Main tasks:

- initialization of hardware components
- Wi-Fi connection
- sensor measurements
- timestamp generation using RTC
- OLED display updates
- telemetry transmission

Sensor data is collected periodically and transmitted every 60 seconds.

---
## Network Communication

### wifi_connect.py

This module handles wireless network connectivity.

Features:

- Wi-Fi initialization
- automatic connection attempt
- IP address detection
- connection status reporting

Reliable connectivity is required for transmitting data to remote databases.

---
## RTC Driver

### ds1302.py

Driver implementation for the DS1302 Real-Time Clock module.

Provides functionality for:

- reading current date and time
- setting system time
- clock control operations

The RTC module allows the system to maintain timestamps even when network synchronization is unavailable.

---
## Display Driver

### ssd1107_rotated.py

Custom driver implementation for the SSD1107 OLED display.

Features:

- I2C communication
- framebuffer rendering
- display rotation correction
- real-time data visualization

Displayed information includes:

- date and time
- temperature
- humidity
- Wi-Fi status
- database communication status

---
## Sensor Testing

### test.py

Used for UART communication testing with external sensors, including SEN6x environmental sensor modules.

This module is primarily intended for debugging and development purposes.

---
## Data Transmission Logic

Telemetry data contains:

- temperature
- humidity
- timestamp

Data is formatted using line protocol and transmitted via HTTP requests.

Two independent database systems are supported:

- QuestDB
- InfluxDB

This enables performance comparison within the scope of the bachelor thesis.