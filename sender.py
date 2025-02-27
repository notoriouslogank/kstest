import serial
import time

ser = serial.Serial('/dev/tty1', baudrate=115200, bytesize=8, write_timeout=10)

def send_data(data):
    if ser.is_open:
        data = data + '\n'
        ser.write(data.encode('utf-8'))
        ser.flush()
        print(f'Send: {data}')
    else:
        print("Port not open.")


if __name__ == "__main__":
    try:
        while True:
            msg = input("Message: ")
            send_data(msg.encode('utf-8'))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping...")
        ser.close()