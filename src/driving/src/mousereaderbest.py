
from evdev import InputDevice, categorize, ecodes
from select import select

dev = InputDevice('/dev/input/mouse0')


while True:
  r,w,x = select([dev], [], [])
  for event in dev.read():
    if event.type == ecodes.EV_KEY:
      print(categorize(event))
