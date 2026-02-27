![Platform](https://img.shields.io/badge/Platform-Raspberry_Pi_Pico_2_WH-red)
![IoT](https://img.shields.io/badge/Focus-IoT_&_Embedded-important)
![Language](https://img.shields.io/badge/Language-MicroPython-blue)
![Hardware](https://img.shields.io/badge/Hardware-Cytron_Robo_Pico_Pro-orange)
![Project](https://img.shields.io/badge/Type-Bachelor_Project-success)

# 🌍 IoT Air Quality Monitoring System

Engineering IoT project developed using **Raspberry Pi Pico 2 WH mounted on the Cytron Robo Pico Pro platform** as part of a bachelor thesis at the Technical University of Košice (FEI).

The system focuses on **environmental data acquisition, real-time monitoring and telemetry transmission** to time-series databases for further analysis and performance comparison.

---

## 🚀 Project Overview

This project implements an **IoT-based environmental monitoring system** designed to continuously measure temperature and humidity parameters and transmit collected telemetry data to database servers.

The device operates as an autonomous embedded monitoring unit capable of:

* collecting sensor measurements
* generating accurate timestamps using RTC hardware
* displaying system status locally
* transmitting telemetry data over Wi-Fi

Collected data is simultaneously stored in:

* **QuestDB**
* **InfluxDB**

allowing comparison of time-series database performance within the scope of the bachelor thesis research.

---

## ⚙️ System Features

* continuous environmental monitoring
* real-time OLED data visualization
* RTC-based timestamp synchronization
* wireless telemetry transmission
* dual database data storage
* modular embedded hardware architecture

---

## 🧩 Hardware Components

* Raspberry Pi Pico 2 WH microcontroller
* Cytron Robo Pico Pro expansion board
* DS1302 Real-Time Clock (RTC)
* SSD1107 OLED Display (128×128)
* DHT22 environmental sensor
* Integrated Wi-Fi connectivity

---

## 🔄 System Workflow

1. Environmental sensors collect measurement data.
2. Raspberry Pi Pico processes sensor readings.
3. RTC module provides accurate timestamps.
4. Measurements are displayed on OLED screen.
5. Data is transmitted via Wi-Fi network.
6. Telemetry is stored in QuestDB and InfluxDB databases.

---

## 🛠 Technologies

* MicroPython
* Embedded Systems Programming
* IoT Architecture
* HTTP Telemetry Communication
* Docker-based Database Deployment
* Time-Series Databases (QuestDB / InfluxDB)

---

## 📂 Project Structure

```
docs/        System documentation and thesis materials
firmware/    MicroPython firmware running on the device
```

---

## 🎓 Academic Context

Bachelor Thesis Project
Faculty of Electrical Engineering and Informatics
Technical University of Košice

---

👨‍💻 Author: **Dmytro Isai**

## 📄 License

MIT License
