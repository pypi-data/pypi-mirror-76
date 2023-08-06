import os
import sys
import time
import struct
import socket
from datetime import datetime as dt
import warnings
import logging

_MAX_TO_PROCESS = 10000000

from wishpy.wireshark.lib.dissector import WishpyDissectorFile
from wishpy.wireshark.lib.dissector import setup_process, cleanup_process

if __name__ == '__main__':

    logger = logging.getLogger()
    logging.basicConfig()

    if not len(sys.argv) >= 2:
        print("Usage: tshark.py <filepath>")
        sys.exit(1)

    input_filepath = sys.argv[1]

    setup_process()

    dissector = WishpyDissectorFile(input_filepath)

    then = dt.now()

    try:
        for dissected in dissector.run(count=0, skip=0):
            print(dissected)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)
    finally:
        cleanup_process()
