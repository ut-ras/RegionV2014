def intialization():
  double forwardDistance = 0;
  # make a the current location
  # use of lidar stay in a certain
  # distance
  # as the bottom left
  return forwardDistance
  
def finishCourse():
    double forwardDistance = intialization();
    int wallsPassed = 0;
    int repeats = 0;
    int oilRigNum = 0;
    oilRigNum = goToBlocks();
    int halt = 0;
     # it will go left and or right
     # oveerall its going to do the overall movement
    forwardDistance = goThroughMaze(wallsPassed,forwardDistance);
    # goLeft(goneForward);
    putblockin(oilRigNum);
    returnToStart(forwardDistance);
    ## when it goes straight
    ## its actually just hugging 
    ## wall and stays between a
    ## max and a min
return;      
    

# and faces them
def goToBlocks():
  boolean blockGrabbed = false;
  int oilRigNum = 0;
  oilRigNum = intialRight();
  turnright();
  turnright();
  while(!blockgrabbed):
    stop();
    blockgrabbed = #subscribe to pickup
  turnleft();
  turnleft();
return oilRigNum;
 

## at the beginning,
## it will move the robot right,
## and go to the middle to take 
## the picture.
def intialRight():
  # modify this go right so it doesnt go up
  double min = ??;
  int fireNumber = 0;
  boolean takenPic = false;
  #publish to move right
  #subscribe to mouse
  while( subscribe to mouse for a certain distance):
    #subscribe to lidar;
    if( lidardata < min):
     goBack();
    if(# subscribe to mouse and if we are middle && !takenPic):
      stop();
      # publish that we have reached the center
      while( fireNumber == 0):
        fireNumber = # subscribe to fireman so we know pic is taken
        # gives us which fire is up

    #publish to move right
  stop();
return fireNumber;


        
## it will go right, and if it finds the 
## distance larger than max
## it will go forward and will add that a 
## wall has been passed     
def goRight(int wallsPassed, double forwardDistance):
  # same as before
  double min = ??;
  double max = ??;
  double length = #length from mouse farthest right we can go
  #subscribe to mouse
  while(wallsPassed != 3 || subscribe to  mouse to see if we have not gone too far left or right):
    #publish to move right;
    #subscribe to mouse
    if(lidardata < min):
      stop();
      goBack();
    if(lidardata < max):
      stop();
      forwardDistance += lidardata;
      goForward(false);
      wallsPassed++;
    ## stop if it can not go any farther to the right
    if(subscribe to mouse for length == length):
      stop();
      forwardDistance = goLeft( timesgoneForward, forwardDistance);
return forwardDistance;


def goLeft(int timesgoneForward, double forwardDistance):
  double max = ??
  double min = ??
  #publish to move left;
  #subscribe to mouse
  while(timesgoneForward != 3 || subscribe to  mouse to see if we have not gone too far left or right):
   #publish to move left;
   #subscribe to mouse 
    if(lidardata < min):
      stop();
      goBack();
    if(lidardata < max):
      stop();
      forwardDistance += lidardata;
      ## is the lidardata sending in some data that can be converted
      goForward(false);
      timesgoneForward++;
    if(subscribe to mouse for length == 0):
      stop();
      forwardDistance = goRight(timesgoneForward, forwardDistance);
return forwardDistance;
    
 ## makes the robot go back a safe distance if it is too close
 ## to the wall
def goBack(double min):
  double min = ??
  double value = lidar length
  #subscribe to lidar
  while ( value < min ): 
    value = #subscribe to lidar
    #publish to move back
  stop();
return;
  
## makes the robot go forward past a wall
## if its the last, you want it to go forward
def goForward(boolean final):
  double max = ??
  if(!final): 
    double value = lidar length  
    while ( value > max ):
      value = #subscribe to lidar
      # publish to move forward
    stop();
  else:
    #publish to move forward
  return;
  
## stops the robot
def stop():
  # publish to both wheels to stop
return;


## goes through maze by starting to go left after the tool has been
## picked up
def goThroughMaze(int timesgoneForward, double forwardDistance):
  forwardDistance = goLeft( timesgoneForward, forwardDistance);
return forwardDistance;




## moves forward to put the block in
def putBlockIn(int oilRigNum):
  boolean inserted = false;
  double max = ??
  #publish wheels to go left
  int oilRig = 0;
  while(lidardata > 0):
    #publish to go left 
  stop();
  while(oilRig != oilRigNum):
    #publish to go right;
  stop();
  while ( !inserted ):
    #publish to insert
    #subscribe to lidar
    if( lidardata > max)
        goForward();
    stop();
return;

## makes the robot go back to the start after
## the block has been placed
def returnToStart(double forwardDistance):
  turnleft();
  turnleft();
  forwardDistance = returnRight(0, forwardDistance);
  gotoBeginning();
return;

## while we were moving we calc'ed distance moved forward
## so we move back at the end the amount remaining
def FinalForward(double forwardDistance):
  double intial = #subscribe from lidar;
  double final = #scribed from lidar;
  while(intial - final != forwardDistance):
    goForward(true);
    final = #subscribe from lidar

  stop();
return;

## goes right till we reached the start position
def goToBeginning():
  # subscribe to mouse
  while( length > #mouse length):
    #publish to go right
  stop();
return;

def returnLeft(int wallsPassed, double forwardDistance):
  double max = ??
  double min = ??
  boolean last = false;
  #publish to move left;
  #subscribe to mouse
  while(wallsPassed != 3 || subscribe to  mouse to see if we have not gone too far left or right):
   #publish to move left;
   #subscribe to mouse 
    if(lidardata < min):
     stop();
      goBack();
    if(lidardata < max):
      stop();
      forwardDistance -= lidardata;
      ## is the lidardata sending in some data that can be converted
      if(!last):
        goForward(false);
      else:
        finalForward(forwardDistance);
      wallsPassed++;
      if(wallsPassed == 2):
        last = true;

    if(subscribe to mouse for length == 0):
      stop();
      forwardDistance = goRight(timesgoneForward, forwardDistance);
return forwardDistance;

def returnRight(int wallsPassed, double forwardDistance):
  # same as before
  double min = ??;
  double max = ??;
  boolean last = false;
  int length = #length from mouse farthest right we can go
  #subscribe to mouse
  while(timesgoneForward != 3 || subscribe to  mouse to see if we have not gone too far left or right):
    #publish to move right;
    #subscribe to mouse
    if(lidardata < min):
      stop();
      goBack();
    if(lidardata < max):
      stop();
      forwardDistance -= lidardata;
      if(!last):
        goForward(false);
      else:
        finalForward(forwardDistance);
      wallsPassed++;
      if(wallsPassed == 2):
        last = true;
    if(subscribe to mouse for length == length):
      stop();
      forwardDistance = goLeft( timesgoneForward, forwardDistance);
return forwardDistance;
#!/usr/bin/env python2

import rospy
import roslib


def main():
    rospy.init_node('pathing')

    while not rospy.is_shutdown():
        rospy.loginfo('hello')
        rospy.sleep(1)


if __name__ == "__main__":
    main()
