import sys
import argparse
from os import path
from time import sleep
import serial
from rich import print

BAUDRATE = 115200

parser = argparse.ArgumentParser(description="Listen for ks-tester info.")
parser.add_argument(
    "-a", "--attempts", metavar="[int]", type=int, default=10, help="Number tries to receive data; defaults to 10",
    dest="attempts"
)
parser.add_argument(
    "-p",
    "--port",
    metavar="[PORT]",
    type=str,
    default="/dev/ttyS0",
    help="Specify a COM port; defaults to /dev/ttyS0",
    dest="port",
)

def get_attempts(args):
    attempts = args.attempts
    return attempts

def get_port(args):
    port = path.join(args.port)
    return port

def await_data(port):
    conn = serial.Serial(port=port, baudrate=BAUDRATE)
    print(f"Connected to {conn}...\n")
    data = conn.readline().decode(encoding='utf-8')
    with open("info.txt", 'a') as outfile:
        outfile.write(f"{data}")
    conn.close()

if __name__ == "__main__":
    args = parser.parse_args()
    port = get_port(args)
    attempts = get_attempts(args)
    counter = 0
    while attempts > counter:
        try:
            sleep(1)
            counter += 1
            if (counter % 5) == 0:
                print(f"Attempt {counter}/{attempts}")
            await_data(port)
        except FileNotFoundError as e:
            print(f"The port {port} does not appear to exist. Please check that you have the correct port information.")
            sys.exit()
        except serial.SerialException as e:
            print(f"Error establishing a connection with serial port {port}:\n{e}\nRetrying...")
    sys.exit(f"Reached attempt limit: {counter}")
