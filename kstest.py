import argparse
import logging

import serial
from rich import print
from rich.logging import RichHandler

FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 112500
DEFAULT_TIMEOUT = 2
BYTES_TO_READ = 64

logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RichHandler(rich_tracebacks=True, markup=True),
        logging.FileHandler("kstest.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog="kstest",
    description="Dead-simple read-only interface for KS Cryptominer Hardware Tester Thing",
    epilog="WU TANG CLAN AIN'T NOTHIN' TO FUCK WITH",
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
parser.add_argument(
    "-f",
    "--file",
    type=str,
    default=None,
    help="Destination path for output file if provided",
    required=False,
)


def get_tty_info(args):
    return args.port, args.baud, args.timeout


def outfile_flag(args):
    return args.file if args.file else False


def create_serial_connection(port, baudrate, timeout):
    try:
        tty_object = serial.Serial(port)
        tty_object.baudrate = baudrate
        tty_object.bytesize = 8
        tty_object.parity = serial.PARITY_NONE
        tty_object.stopbits = serial.STOPBITS_ONE
        tty_object.timeout = timeout
        logger.info(f"Created serial connection:\n{tty_object}")
        return tty_object
    except serial.SerialException as e:
        logger.error(f"Failed to create serial connection: {e}")
        return None


def main_loop(port_name, baudrate, timeout):
    tty_object = create_serial_connection(port_name, baudrate, timeout)
    if tty_object is None:
        logger.critical("Exiting due to serial connection failure.")
        exit(1)

    try:
        received_data = tty_object.read(BYTES_TO_READ)
        print(received_data.decode())
        if outfile:
            logger.info(f"Outputting data to {outfile}...")
            with open(outfile, "wb") as f:
                f.write(received_data)
            print(f"Wrote outfile -> {outfile}")
    except serial.SerialException as e:
        logger.error(f"Serial communication error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    logger.debug("Program start.")
    args = parser.parse_args()
    logger.debug(f"Parsed the following args: {args}")
    port_name, baudrate, timeout = get_tty_info(args)
    outfile = outfile_flag(args)
    while True:
        main_loop(port_name, baudrate, timeout)
    # tty_object = create_serial_connection(port_name, baudrate, timeout)
    # if tty_object is None:
    #    logger.critical("Exiting due to serial connection failure.")
    #    exit(1)

    # print(f"Checking port {args.port} for incoming data -> {tty_object}")
    # while True:
    #    try:
    #        received_data = tty_object.read(BYTES_TO_READ)
    #        print(received_data.decode())
    #        if outfile:
    #            logger.info(f"Outputting data to {outfile}...")
    #            with open(outfile, "wb") as f:
    #                f.write(received_data)
    #            print(f"Wrote outfile -> {outfile}")
    #    except serial.SerialException as e:
    #        logger.error(f"Serial communication error: {e}")
    #        False
    #    except Exception as e:
    #        logger.error(f"Unexpected error: {e}")
    #        True
