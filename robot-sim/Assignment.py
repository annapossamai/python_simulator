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

    dist=1000
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
            codeS=token.info.code
    if dist==1000:
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
    distG=1000
    for token in R.see():
        if token.dist < distG and token.info.marker_type is MARKER_TOKEN_GOLD:
            distG=token.dist
            rotG_y=token.rot_y 
            codeG=token.info.code
    if distG==1000:
        return -1, -1, -1
    else:
        return distG, rotG_y, codeG

def GoToGolden():
    """
    Function to check the presence of the closest golden token and to release the silver token near to the golden token found.
    """
    a=1
    while a==1:
        distG, rotG_y, codeG= find_golden_token()
        if (codeG==-1):
            turn(20,0.5)
        elif(codeG not in listG and codeG !=-1):
            print("the Golden code is:",codeG)
            b=1
            while (distG>=d_th and b is 1):
                distG, rotG_y, codeG= find_golden_token()
                if distG==-1:
                    print("I don't see any golden token!")
                    turn(+20,1)
                if distG<(d_th+0.4):
                    print("Here we are")            
                    R.release()
                    print("iniziale golden: ", listG)
                    listG.append(codeG)
                    print("finale golden: ", listG)
                    print("Token released!")
                    b=2
                    a=2
                elif-a_th<=rotG_y<=a_th:
                    #print("Ah, I will drive a bit ahead")
                    drive(100,0.2)
                elif rotG_y<-a_th:
                    print("Turn left a bit")
                    turn(-2,0.5)
                elif rotG_y> a_th:
                    print("Turn right a bit")
                    turn(2,0.5)
        else:
            print("golden era in lista!", listG)
            turn(2,0.5)         

#The first step is the control of the variable `cont` that indicates the number of steps 
#necessary to reach a more than 360 degrees angle (at the setted speed and seconds (20,0.5)). 
#This allows to have at least a 360 degrees view of the arena.


#The program starts with the initialization of two vector lists ( `listS`, `listG`) 
#and a control variable (`cont`).The list `listS` registers the silver token grabbed by the robot
#and  the `listG` registers the golden token near the silver token released.

cont=0      #counter for ending the program (it counts how many turns the robot does without see anything)
listS=[]
listG=[]
while 1:
    if (cont==12):  #`cont` that indicates the number of steps necessary to reach a more than 360 degrees angle (at the setted speed and seconds (20,0.5)). 
                    #This allows to have at least a 360 degrees view of the arena.     
        print("END")
        exit()
    dist, rot_y, codeS= find_silver_token() #the robot find the closest silver token 
    if codeS not in listS:     # to avoid bringing silver token already paired. 
        if dist==-1:    #If the robot can't see any silver token (`dist=-1`) then it will turn and the counter will increase its value.
            print("I don't see any silver token!")
            turn(20,0.5)
            cont=cont+1
        #The following "elif" are more steps to check the proximity of the silver token.
        elif dist<d_th: # the robot is well aligned with the token
            print("I found a silver token!")
            cont=0
            if R.grab():
                print("Gotcha!")
                listS.append(codeS)
                GoToGolden()
                drive(-20,1)
                turn(30,1)
        elif -a_th<=rot_y<=a_th:
            print("Ah, that I'll do")
            drive(80,0.2)
        elif rot_y<=-a_th:
            print("Left a bit")
            turn(-2,0.5)
        elif rot_y>= a_th:
            print("Right a bit")
            turn(2,0.5)
        else:
            print("Maybe there is a problem!")      #flag for debug
    else:
        print("Already associated!")
        turn(20,0.5)
        cont=cont+1
        