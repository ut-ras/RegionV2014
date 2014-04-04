from evdev import InputDevice
from select import select
from pycopia.OS.Linux.IOCTL import _IOC, _IO, _IOW, _IOR, _IOC_READ

dev = InputDevice('/dev/input/mouse0')

while True:
   r,w,x = select([dev], [], [])
   for event in dev.read():
       print(event)

# event at 1337427573.061822, code 01, type 02, val 01
# event at 1337427573.061846, code 00, type 00, val 00
