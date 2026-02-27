# System Architecture

The IoT Air Quality Monitoring System is designed to collect environmental data using a microcontroller device and transmit measurements to time-series databases for storage and analysis.

## Architecture Overview

Sensor → Microcontroller → Wi-Fi → Server → Database

The system consists of the following components:

### 1. Sensor Layer

Environmental data is collected using sensors connected to the Raspberry Pi Pico.

Measured parameters:

- Temperature
- Humidity

The DHT22 sensor is used for environmental monitoring.

---

### 2. Processing Layer

The Raspberry Pi Pico (Cytron Robo Pico) performs:

- Sensor data acquisition
- Timestamp synchronization using RTC DS1302
- OLED visualization
- Network communication

MicroPython firmware is used as the main runtime environment.

---

### 3. Time Synchronization

The DS1302 Real-Time Clock module provides accurate timestamps independent from network availability.

This ensures reliable data logging even during temporary
Wi-Fi disconnections.

---

### 4. Visualization

SSD1107 OLED display provides real-time information:

- Current date and time
- Temperature
- Humidity
- Wi-Fi connection status
- Database transmission status

---

### 5. Communication Layer

The device connects to a local Wi-Fi network and sends telemetry data using HTTP requests.

Data transmission interval:

60 seconds.

---

### 6. Data Storage Layer

Collected measurements are transmitted simultaneously to:

- QuestDB
- InfluxDB

Both databases are deployed using Docker containers on a local server.

This allows comparison of performance and financial efficiency between time-series databases.