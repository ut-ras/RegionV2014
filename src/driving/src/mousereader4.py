import struct
import time
import sys

infile_path = "/dev/input/mouse0"

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)

xsum = 0
ysum = 0

while event:
    (tv_sec, tv_usec, typ, code, value) = struct.unpack(FORMAT, event)

    if typ != 0 or code != 0 or value != 0:
        print("Event type %u, code %u, value: %u at %d, %d" % \
            (typ, code, value, tv_sec, tv_usec))
        xsum += tv_sec
        ysum += tv_usec
        print xsum, ysum
    else:
        # Events with code, type and value == 0 are "separator" events
        print("===========================================")

    event = in_file.read(EVENT_SIZE)

in_file.close()
