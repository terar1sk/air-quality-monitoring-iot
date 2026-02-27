# Database Setup

## Overview

The IoT monitoring system stores collected telemetry data in two different time-series databases.

The purpose of using two databases is to compare their performance, ingestion speed and operational efficiency for IoT workloads.

Databases are deployed locally using Docker containers.

---

## Database Architecture

Data flow:

Sensor → Raspberry Pi Pico → Wi-Fi → Server → Database

Telemetry data is transmitted simultaneously to:

- QuestDB
- InfluxDB

---

## QuestDB

QuestDB is used as a high-performance time-series database optimized for fast data ingestion.

Default configuration:

Port: 9000

QuestDB receives data using HTTP requests formatted
with line protocol.

Example record:

sensor_data,device=pico temperature=24.1,humidity=52.3 1735678000000000000

Stored parameters:

Fields:

- temperature
- humidity

Tag:

- device identifier

Timestamp precision:

nanoseconds.

---
## InfluxDB

InfluxDB is used for comparison with QuestDB as a widely adopted IoT time-series database.

Default API port:

8086

Configuration parameters:

- Organization
- Bucket
- API Token

Data is written using HTTP API v2.

Example request includes:

- measurement name
- tags
- fields
- timestamp

---
## Data Transmission Interval

Sensor measurements are transmitted every:

60 seconds.

This interval provides stable data collection while minimizing network load.

---
## Deployment Environment

Both databases are deployed using Docker containerson a local server machine.

Advantages:

- easy deployment
- environment isolation
- reproducible configuration

Docker allows quick database initialization during testing and experimentation.

---
## Data Usage

Stored telemetry data can be used for:

- performance comparison
- long-term environmental monitoring
- visualization dashboards
- statistical analysis