import sys, os, struct, time, fcntl, mousedev, usbhid
from pycopia.aid import Queue
from pycopia.OS.Linux.IOCTL import _IOC, _IO, _IOW, _IOR, _IOC_READ

INT = "i"
INT2 = "ii"

EVIOCGKEYCODE   = _IOR(69, 0x04, INT2)
EVIOCGKEY       = _IOR(69, 0x05, INT2)


