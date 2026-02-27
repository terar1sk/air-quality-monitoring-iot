from machine import Pin, I2C
from ssd1107_rotated import SSD1107
from dht import DHT22
from wifi_connect import connect_wifi
from time import sleep
import network
import usocket as socket
import time
import urequests
from ds1302 import DS1302  # RTC DS1302

# ===================== CONFIG =====================

# --- QuestDB ---
QUESTDB_IP = "192.168.100.5"   # IP Docker + QuestDB
QUESTDB_PORT = 9000

# --- InfluxDB ---
INFLUX_IP = "192.168.100.5"    # IP Docker + InfluxDB
ORG = "home"
BUCKET = "data_from_pico"
TOKEN = "YOUR_TOKEN" # replace with your InfluxDB API token
PRECISION = "s"

INFLUX_URL = (
    f"http://{INFLUX_IP}:8086/api/v2/write"
    f"?org={ORG}&bucket={BUCKET}&precision={PRECISION}"
)

# --- Wi-Fi ---
SSID = "YOUR_WIFI"
PASSWORD = "YOUR_PASSWORD"

# ================== INIT WI-FI ====================

ip = connect_wifi(SSID, PASSWORD)
wlan = network.WLAN(network.STA_IF)

# ================== SENSORS / OLED =================

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1107(128, 128, i2c, addr=0x3C)
sensor = DHT22(Pin(27))

# === RTC (DS1302) ===
rtc = DS1302(clk=2, dio=3, cs=12) # GP2, GP3, GP12

# Один раз выставляешь время, потом строку можно закомментить
# rtc.write_time(2025, 12, 2, 2, 15, 50, 0)
#        год,  мес, день, день_нед, час, мин, сек


# ================== SEND TO QUESTDB =================

def send_to_questdb(temp, hum, ts_ns):
    host = QUESTDB_IP
    port = QUESTDB_PORT

    # measurement sensor_data, tag device=pico, поля temperature/humidity, timestamp ns
    line = f"sensor_data,device=pico temperature={temp},humidity={hum} {ts_ns}\n"

    request = (
        "POST /write?precision=ns HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: MicroPython\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(line)}\r\n"
        "Connection: close\r\n\r\n"
        f"{line}"
    )

    try:
        addr = socket.getaddrinfo(host, port)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(request.encode())
        response = s.recv(1024)
        s.close()

        if b"204" in response or b"200" in response:
            print("✅ QuestDB OK")
            return True
        else:
            print("⚠️ QuestDB response:", response)
            return False
    except Exception as e:
        print("❌ Error sending to QuestDB:", e)
        return False


# ================== SEND TO INFLUXDB =================

def send_to_influx(temp, hum, ts_ns):
    # measurement/tag/fields
    line = f"sensor_data,device=pico temperature={temp},humidity={hum} {ts_ns}"
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "text/plain"
    }
    try:
        r = urequests.post(INFLUX_URL, data=line, headers=headers)
        status = r.status_code
        r.close()
        if status == 204:
            print("✅ InfluxDB OK")
            return True
        else:
            print("⚠️ InfluxDB status:", status)
            return False
    except Exception as e:
        print("❌ Error sending to InfluxDB:", e)
        return False


# ===================== MAIN LOOP ====================

while True:
    try:
        # --- датчик ---
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        # --- время с RTC ---
        # (год, месяц, день, день_нед, час, минута, секунда)
        t = rtc.read_time()
        timestamp = time.mktime((t[0], t[1], t[2], t[4], t[5], t[6], 0, 0))
        ts_ns = int(timestamp * 1_000_000_000)  # наносекунды

        # --- вывод на OLED ---
        oled.fill(0)
        oled.text(
            f"{t[2]:02}.{t[1]:02}.{t[0]} {t[4]:02}:{t[5]:02}:{t[6]:02}",
            0, 16
        )
        oled.text(f"Temp: {temp:.1f} C", 10, 32)
        oled.text(f"Hum:  {hum:.1f} %", 10, 42)

        # --- статус Wi-Fi ---
        if wlan.isconnected() and ip:
            wifi_status = "Wi-Fi OK"
            oled.text(ip or "No IP", 10, 60)
        else:
            wifi_status = "No Wi-Fi"
            oled.text("No IP", 10, 60)

        # --- отправка в обе базы ---
        quest_ok = send_to_questdb(temp, hum, ts_ns)
        influx_ok = send_to_influx(temp, hum, ts_ns)

        # строки статуса
        oled.text(wifi_status, 10, 70)
        oled.text("QDB: " + ("OK" if quest_ok else "ERR"), 10, 85)
        oled.text("|", 66, 85)
        oled.text("INF: " + ("OK" if influx_ok else "ERR"), 73, 85)
        oled.show()

        print(
            f"[{t[4]:02}:{t[5]:02}:{t[6]:02}] "
            f"Temp={temp:.1f}°C, Hum={hum:.1f}%, "
            f"WiFi={wifi_status}, QuestDB={'OK' if quest_ok else 'ERR'}, "
            f"InfluxDB={'OK' if influx_ok else 'ERR'}"
        )

        sleep(60)   # отправка каждые 60 секунд;

    except Exception as e:
        oled.fill(0)
        oled.text("Sensor Error!", 10, 50)
        oled.show()
        print("⚠️ Error:", e)
        sleep(2)