1. Chạy publisher_retained.py → gửi giá trị, retained lưu lại
2. Chạy late_monitor.py → xác nhận vẫn nhận được (như trước)
3. Dừng monitor, chạy python .\clear_retained.py
4. Chạy lại late_monitor.py → lần này sẽ không nhận được gì cho topic đó nữa, dù trước đó đã từng có retained message.