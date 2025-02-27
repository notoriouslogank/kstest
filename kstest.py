import serial
from rich import print


if __name__ == "__main__":
    PORT_NAME = "/dev/ttyUSB0"

    tty_object = serial.Serial(PORT_NAME)
    tty_object.baudrate = 9600
    tty_object.bytesize = 8
    tty_object.parity = serial.PARITY_NONE
    tty_object.stopbits = serial.STOPBITS_ONE
    tty_object.timeout = 60
    print(
        f"Checking port {PORT_NAME} for incoming data.\nConnection will timeout in {tty_object.timeout} seconds."
    )

    received_data = tty_object.read()
    decoded_data = received_data.decode(encoding="ascii")

    output = f"The following data was received; if this data is not correctly decoded, please note that in your bug report: DATA BEGINS\n{decoded_data}"
