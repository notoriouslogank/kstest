import argparse
import logging
import os
import serial
from rich import print
from rich.logging import RichHandler

LOGFILE = "kstest.log"
FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 112500
DEFAULT_TIMEOUT = 2
DEFAULT_BUFFERSIZE = 64

if os.path.exists(LOGFILE):
    os.rename(LOGFILE, f"{LOGFILE}.old")

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
parser.add_argument(
    "-B",
    "--buffersize",
    type=int,
    default=DEFAULT_BUFFERSIZE,
    help="How many bytes to read into the buffer",
    required=False)


def get_tty_info(args):
    logger.debug("Getting tty info.")
    logger.debug(
        f"Parsed the following arguments:{args.port}, {args.baud}, {args.timeout}, {args.buffersize}")
    return args.port, args.baud, args.timeout, args.buffersize


def outfile_flag(args):
    logger.debug("Getting outfile flag.")
    return args.file if args.file else False


def create_serial_connection(port, baudrate, timeout, bytesize):
    logger.debug("Attempting connection...")
    try:
        tty_object = serial.Serial(port)
        tty_object.baudrate = baudrate
        tty_object.bytesize = 8
        tty_object.parity = serial.PARITY_NONE
        tty_object.stopbits = serial.STOPBITS_ONE
        tty_object.timeout = timeout
        tty_object.buffersize = buffersize
        logger.info(f"Created serial connection:\n{tty_object}")
        return tty_object
    except serial.SerialException as e:
        logger.error(f"Failed to create serial connection: {e}")
        logger.critical("Failed to create serial connection: {e}")
        exit(1)


def main_loop(port_name, baudrate, timeout, buffersize):
    logger.debug("Begin main loop.")
    tty_object = create_serial_connection(
        port_name, baudrate, timeout, buffersize)
    logger.debug("Using tty_object: {tty_object}")
    output_line = []

    try:
        logger.debug("Attempting to parse buffer...")
        for c in tty_object.read(buffersize):
            output_line.append(c)
            if c == '\r':
                print("\n" + "".join(output_line))
                output_line = []
                break
#        received_data = tty_object.read(buffersize)
#        print(received_data.decode())
#        if outfile:
#            logger.info(f"Outputting data to {outfile}...")
#            with open(outfile, "wb") as f:
#                f.write(received_data)
#            print(f"Wrote outfile -> {outfile}")
    except serial.SerialException as e:
        logger.critical(f"Serial communication error: {e}")
        tty_object.close()
        exit(1)
    except Exception as e:
        tty_object.close()
        logger.critical(
            f"An unforeseen exception has occured:\nShit's fucked bro: {e}")
        exit(1)
    finally:
        logger.info(f"Closing connection on port {tty_object}")
        tty_object.close()
        exit(0)


if __name__ == "__main__":
    logger.info("Program start.")
    args = parser.parse_args()
    port_name, baudrate, timeout, buffersize = get_tty_info(args)
    outfile = outfile_flag(args)
    logger.debug("Beginning main loop...")
    while True:
        main_loop(port_name, baudrate, timeout, buffersize)
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
