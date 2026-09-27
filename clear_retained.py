import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883

# Danh sách các topic cần xóa retained message (vì lý do bảo mật:
# không muốn subscriber join sau vẫn đọc được giá trị/trạng thái cũ)
TOPICS_TO_CLEAR = [
    "sensor/temp/retained",
    # thêm topic khác nếu cần, ví dụ: "device/status"
]

client = mqtt.Client(client_id="retained_cleaner")
client.connect(BROKER, PORT, keepalive=10)
client.loop_start()
time.sleep(0.5)  # đợi kết nối ổn định trước khi publish

for topic in TOPICS_TO_CLEAR:
    # Cơ chế chuẩn của MQTT để XÓA retained message:
    # publish payload RỖNG (None / b"") với retain=True lên đúng topic đó.
    # Broker sẽ hiểu đây là lệnh "xóa", không lưu lại gì nữa cho topic này.
    result = client.publish(topic, payload=None, qos=1, retain=True)
    result.wait_for_publish()
    print(f"[Cleaner] Đã gửi lệnh xóa retained message trên topic: {topic}")

time.sleep(0.5)
client.loop_stop()
client.disconnect()
print("[Cleaner] Hoàn tất. Từ giờ subscriber join sau sẽ KHÔNG còn nhận được giá trị cũ.")
