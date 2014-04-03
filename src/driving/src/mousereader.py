import struct

file = open( "/dev/input/mouse1", "rb" )

xsum = 0
ysum = 0

def getMouseEvent():
  buf = file.read(3)
  x,y = struct.unpack( "bb", buf[1:] )
  print ("x: %d, y: %d" % (x, y) )
  return x,y
  # return stuffs


while(1):
  x,y = getMouseEvent()
  xsum += x
  ysum += y
  print xsum, ysum, '\n'

file.close()

