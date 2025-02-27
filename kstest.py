import serial
from rich import print
import argparse


DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 9600
DEFAULT_TIMEOUT = 60

parser = argparse.ArgumentParser(
    prog="kstest",
    description="Dead-simple read-only interface for KS Cryptominer Hardware Tester Thing",
    epilog="idk what this field is lol",
)
parser.add_argument(
    "-p",
    "--port",
    type=str,
    help="Specify an arbitrary port; if unspecified",
    default=DEFAULT_PORT,
    required=False,
)
parser.add_argument(
    "-b",
    "--baud",
    type=int,
    default=DEFAULT_BAUDRATE,
    help="Specify incoming baudrate for data stream",
    required=False,
)
parser.add_argument(
    "-t",
    "--timeout",
    type=int,
    default=DEFAULT_TIMEOUT,
    help="The amount of time to listen when no connection is forthcoming",
    required=False,
)

parser.add_argument("-f", "--file", type=str, help="Name of outfile", required=False)


def get_tty_info(args):
    port_name = args.port
    baudrate = args.baud
    timeout = args.timeout
    return port_name, baudrate, timeout


def outfile_flag():
    if args.file:
        filename = args.file
        return filename
    else:
        return False


if __name__ == "__main__":
    args = parser.parse_args()
    port_name, baudrate, timeout = get_tty_info(args)
    outfile = outfile_flag()

    tty_object = serial.Serial(port_name)
    tty_object.baudrate = baudrate
    tty_object.bytesize = 8
    tty_object.parity = serial.PARITY_NONE
    tty_object.stopbits = serial.STOPBITS_ONE
    tty_object.timeout = 60

    print(f"Checking port {args.port} for incoming data -> {tty_object}")

    received_data = tty_object.read()
    decoded_data = received_data.decode(encoding="ascii")

    if outfile != False:
        with open(outfile, "w") as f:
            f.write(decoded_data)
        print(f"Wrote outfile -> {outfile}")
    else:
        output = f"The following data was received; if this data is not correctly decoded, please note that in your bug report: DATA BEGINS\n{decoded_data}"
