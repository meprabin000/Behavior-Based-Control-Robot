#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
from random import random


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# defining sensors
LM = Motor(Port.A)
RM = Motor(Port.B)
USS = UltrasonicSensor(Port.S1)
CS = ColorSensor(Port.S2)
TSR = TouchSensor(Port.S3)
TSL = TouchSensor(Port.S4)

# configurations
slight_movement_speed = 100
slight_turn_speed = 50

move_time = 1000
turn_time = 1000



# historical data
move_history = []
USS_history = []
TS_history = []

history_length = 5

################# WALL FOLLOWER #####################

def good_distance():
    return USS.distance() < 70

def add_sensor_history():
    USS_history.append(USS.distance())
    TS_history.append((TSR.pressed(), TSL.pressed()))

    if len(USS_history) == history_length: USS_history.pop(0)
    if len(TS_history) == history_length: TS_history.pop(0)

def add_move_history(move):
    move_history.append(move)
    if len(move_history) == history_length: move_history.pop(0)

def clear_history():
    USS_history = list()
    TS_history = list()

def goal_found():
    return CS.color() == Color.GREEN

def extinguish():
    pass

# detect if the wall is in the front
def wall_front():
    return True if TSR.pressed() and TSL.pressed() else False

# detect if the wall is on the left
def wall_left():
    return True if USS.distance() < 300 else False

# moves the robot forward in the given speed
def slight_forward():
    time.sleep(move_time/1000+0.5)
    LM.run_time(slight_movement_speed, move_time, Stop.COAST, False)
    RM.run_time(slight_movement_speed, move_time, Stop.COAST, False) 

def slight_backward():
    time.sleep(move_time/1000+0.5)
    LM.run_time(-slight_movement_speed,move_time,Stop.HOLD,False)
    RM.run_time(-slight_movement_speed,move_time,Stop.HOLD,False)

def slight_right():
    time.sleep(turn_time/1000+0.5)
    LM.run_time(slight_turn_speed, turn_time, Stop.COAST, False)
    RM.run_time(-slight_turn_speed, turn_time, Stop.COAST, False)    

def slight_left():
    time.sleep(turn_time/1000+0.5)
    LM.run_time(-slight_turn_speed, turn_time, Stop.COAST, False)
    RM.run_time(slight_turn_speed, turn_time, Stop.COAST, False) 

def very_slight_right():
    time.sleep(turn_time/1000+0.5)
    LM.run_time(slight_turn_speed, turn_time/2, Stop.COAST, False)
    RM.run_time(-slight_turn_speed, turn_time/2, Stop.COAST, False)    

def very_slight_left():
    time.sleep(turn_time/1000+0.5)
    LM.run_time(-slight_turn_speed, turn_time/2, Stop.COAST, False)
    RM.run_time(slight_turn_speed, turn_time/2, Stop.COAST, False) 

def prev_move():
    return move_history[-1]

def log(message, pair = None):
    if pair == None:
        print("---------", message, "-----------")
    else:
        print(message, ": ", pair)

def print_sensor_readings():
    log("USS sensor: ", USS.distance())
    log("Touch sensor Right: ", TSR.pressed())
    log("Touch sensor Left: ", TSL.pressed())
    log("Color Sensor: ", CS.color())

# follow the wall
def follow_wall():
    wander_step = 10
    current_step = 0
    while True:
        time.sleep(2)
        if goal_found():
            extinguish()

        elif TSL.pressed() and TSR.pressed():
            log("Full wall hit")
            slight_backward()
            print_sensor_readings()
            for i in range(3): slight_right()
            slight_forward()
            add_move_history("right")

        elif TSR.pressed():
            log("Right edge hit")
            slight_backward()
            for i in range(3): slight_right()
            slight_forward()
            add_move_history("right")
        
        elif TSL.pressed():
            log("Left edge hit")
            slight_backward()
            slight_right()
            slight_forward()
            add_move_history("right")

        elif wall_left():
            log("Wall on the left")
            if USS.distance() < 30: very_slight_right()
            elif USS.distance() > 120: 
                for i in range(USS.distance() // 100): 
                    very_slight_left()
                    slight_forward()
            if random() > 0.98:
                slight_backward()
            
            slight_forward()
            add_move_history("forward")

        elif USS.distance() < 150 and prev_move() == "right":
            log("Prev move right")
            slight_right()
            slight_forward()
            slight_forward()
            add_move_history("right")
            
        else:
            log("Else condition")
            if random() < 0.8:
                for i in range(3): slight_left()
                for i in range(2): slight_forward()
            else: # wander straight
                for i in range(2): slight_forward()

        current_step += 1
        print_sensor_readings()


def test_sensor():
    while True:
        log("Color sensor: ", CS.color())
        time.sleep(2)


        

follow_wall()
#test_sensor()

# Write your program here.
ev3.speaker.beep()
