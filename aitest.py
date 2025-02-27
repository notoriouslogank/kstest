import serial
import time

ser = serial.Serial('COM1', 9600)

# Send data
data_to_send = "Ping"
ser.write(data_to_send.encode())
print(f"Sent: {data_to_send}")

# Wait for a response (adjust the timeout as needed)
time.sleep(1)

# Receive data
if ser.in_waiting > 0:
    received_data = ser.readline().decode().strip()
    print(f"Received: {received_data}")
else:
    print("No data received")

ser.close()