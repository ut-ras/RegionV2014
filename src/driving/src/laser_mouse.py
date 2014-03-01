from evdev  import InputDevice, categorize, ecodes
from select import select
dev = InputDevice('/dev/input/event5')

print(dev) 

#abs_x = ''

while True:
    r,w,x = select([dev], [], [])
    for event in dev.read():
        if event.type == ecodes.EV_REL:
            print(ecodes.EV_REL)
