import paho.mqtt.client as mqtt
import csv
import time
import os

BROKER = "localhost"
PORT = 1883

TOPIC_RETAINED = "sensor/temp/retained"
TOPIC_NORMAL = "sensor/temp/normal"
TOPIC_DEVICE_STATUS = "device/status"  # để log luôn cả phần LWT nếu muốn test chung

CSV_FILE = "mqtt_test_log.csv"

# Tạo file CSV với header nếu chưa tồn tại
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "received_timestamp", "topic", "qos", "retain_flag",
            "payload_raw", "send_timestamp", "staleness_ms"
        ])

def log_to_csv(row):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[Late Monitor] Connected (rc={rc}). Đang lắng nghe...")
    client.subscribe(TOPIC_RETAINED, qos=1)
    client.subscribe(TOPIC_NORMAL, qos=1)
    client.subscribe(TOPIC_DEVICE_STATUS, qos=1)

def on_message(client, userdata, msg):
    recv_time = time.time()
    raw = msg.payload.decode()
    send_time = None
    staleness_ms = None

    # Cố gắng tách "value|send_time" nếu có; nếu không parse được thì để trống
    if "|" in raw:
        try:
            _, send_time_str = raw.split("|", 1)
            send_time = float(send_time_str)
            staleness_ms = round((recv_time - send_time) * 1000, 1)
        except ValueError:
            pass

    tag = "RETAINED" if msg.retain else "LIVE"
    print(f"[{tag}] topic={msg.topic} payload={raw} retain={msg.retain} "
          f"staleness_ms={staleness_ms}")

    log_to_csv([
        recv_time, msg.topic, msg.qos, msg.retain,
        raw, send_time, staleness_ms
    ])

client = mqtt.Client(client_id="late_join_monitor")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=10)
client.loop_forever()