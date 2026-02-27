from machine import UART
import time

uart = UART(
    1,
    baudrate=115200,
    bits=8,
    parity=None,
    stop=1,
    tx=4,
    rx=5,
    timeout=1000
)

print("Receiving data from SEN63C...")

while True:
    if uart.any():
        data = uart.read()
        if data:
            print(data)
    time.sleep(0.2)
