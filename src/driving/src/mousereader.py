import struct

file = open( "/dev/input/mouse1", "rb" )

time = 0
xset = list()
yset = list()

def getMouseEvent(t):
  buf = file.read(3)
  x,y = struct.unpack( "bb", buf[1:] )
  print ("t: %d, x: %d, y: %d\n" % (t, x, y) )
  # return stuffs

  xset.append(x)
  yset.append(y)

while( time < 10  ):
  getMouseEvent(time)
  time+=1
file.close()
print(xset)
print(yset)
print('\nreverse coordinates:')
xset.reverse()
yset.reverse()
print(xset)
print(yset)

