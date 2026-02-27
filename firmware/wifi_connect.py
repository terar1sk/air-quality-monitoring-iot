import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        for _ in range(20):
            if wlan.isconnected():
                break
            print(".", end="")
            time.sleep(0.5)
    if wlan.isconnected():
        print("\n✅ Connected to Wi-Fi")
        print("IP:", wlan.ifconfig()[0])
        return wlan.ifconfig()[0]
    else:
        print("\n❌ Failed to connect")
        return None