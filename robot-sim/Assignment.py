from __future__ import print_function

import time
from sr.robot import *

"""
run with:
    python2 run.py assigment.py
"""



R = Robot()
""" instance of the class Robot"""

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args:   speed (int): the speed of the wheels
            seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args:   speed (int): the speed of the wheels
            seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
        dist (float): distance of the closest silver token (-1 if no silver token is detected)
        rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
            codeS=token.info.code
    if dist==100:
        return -1, -1, -1
    else:
           return dist, rot_y, codeS


def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
    dist (float): distance of the closest golden token (-1 if no golden token is detected)
    rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    distG=100
    for token in R.see():
        if token.dist < distG and token.info.marker_type is MARKER_TOKEN_GOLD:
            distG=token.dist
            rotG_y=token.rot_y 
            codeG=token.info.code
    if distG==100:
        return -1, -1, -1
    else:
        return distG, rotG_y, codeG

def GoToGolden():
    """
    Function to check the presence of the closest golden token and to release the silver token near to it.
    """
    a=1 # constant to end the while loop
    while a==1:
        distG, rotG_y, codeG= find_golden_token() # the robot looks for a golden token
        if (codeG==-1):
            turn(20,0.5)
        elif(codeG not in listG and codeG !=-1): # Control to avoid bringing golden token already paired
            print("the Golden code is:",codeG)
            b=1 # constant to end the while loop
            while (distG>=d_th and b is 1):
                distG, rotG_y, codeG= find_golden_token()
                if distG==-1: # if no token is detected, the robot will turn 
                    print("I don't see any golden token!")
                    turn(+20,1)
                if distG<(d_th+0.4): # if the robot closes to the golden token, it releases the silver token in that position and registers the codeG within listG
                    print("Here we are")            
                    R.release()
                    # print("iniziale golden: ", listG)
                    listG.append(codeG)
                    # print("finale golden: ", listG)
                    print("Token released!")
                    b=2     # end the second while loop
                    a=2     # end the first while loop
                elif-a_th<=rotG_y<=a_th: # if the robot is well aligned with the token, it goes forward
                    print("Ah, I'll go on a bit")
                    drive(100,0.2)
                elif rotG_y<-a_th: # if the robot is not well aligned with the token, it will turn on the left or on the right
                    print("Turn left a bit")
                    turn(-2,0.5)
                elif rotG_y> a_th:
                    print("Turn right a bit")
                    turn(2,0.5)
        else:   # if codeG is in listG the robot will turn a bit
            print("The golden token was already included in the listG!")
            turn(2,0.5)         


cont=0      # Counter for ending the program (it counts how many turns the robot does without see anything)
listS=[]    # registers the silver token grabbed by the robot
listG=[]    # registers the golden token near the silver token released.
while 1:
    if (cont==12):  # 12 is the number of steps required to reach a more than 360 degrees angle (at the setted (speed,seconds)=(20,0.5)). 
                    # This allows to have at least a 360 degrees view of the arena.     
        print("END")
        exit()
    dist, rot_y, codeS= find_silver_token()    # the robot find the closest silver token 
    if codeS not in listS:  # control to avoid bringing silver token already paired. 
        if dist==-1:        # if the robot can't see any silver token (`dist=-1`) then it will turn and the counter will increase its value.
            print("I don't see any silver token!")
            turn(30,0.5)
            cont=cont+1
        # The following "elif" are steps to check the proximity of the found silver token.
        elif dist<d_th: # when the robot is close to the silver token, it grabs it and goes to the nearest golden token (via GoToGolden()) and then it moves away
            print("I found a silver token!")
            cont=0
            if R.grab():
                print("Gotcha!")
                listS.append(codeS)
                GoToGolden()
                drive(-20,1)
                turn(30,1)
        elif -a_th<=rot_y<=a_th: # if the robot is well aligned with the token, it goes forward
            print("Ah, that I'll do")
            drive(80,0.2)
        elif rot_y<=-a_th: # if the robot is not well aligned with the token, it will turn on the left or on the right
            print("Left a bit")
            turn(-2,0.5)
        elif rot_y>= a_th:
            print("Right a bit")
            turn(2,0.5)
        else:
            print("Maybe there is a problem!")      # Flag for debug
    else:   # if codeS is in listS then the robot will turn and the couner will increase its value
        print("Already associated!")
        turn(20,0.5)
        cont=cont+1
        