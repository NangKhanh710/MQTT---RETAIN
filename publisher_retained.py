import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883

TOPIC_RETAINED = "sensor/temp/retained"
TOPIC_NORMAL = "sensor/temp/normal"

client = mqtt.Client(client_id="temp_sensor_01")
client.connect(BROKER, PORT, keepalive=10)

# message 

value = "50"
send_time = time.time()
payload = f"{value}|{send_time}"

print(f"[Publisher] Publishing temperature = {value}°C at {send_time}...")
client.publish(TOPIC_RETAINED, payload, qos=1, retain=True)
client.publish(TOPIC_NORMAL, payload, qos=1, retain=False)

print("[Publisher] Done. Disconnecting now...")
client.disconnect()