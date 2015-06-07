__author__ = 'muzcategui'
# Filename: Car.py

import math
import numpy as np

#constants
BETA = 0.75 #reaction time
SIGMA = 0.0070104 # reciprocal of twice the maximum average deceleration of the following vehicle
MIN_ACCELERATION = 0 # minimum acceleration
MAX_ACCELERATION = 5 # maximum acceleration
MIN_SPEED = (50*1.6)*1000/3600 # minimum vehicle speed in m/s
MAX_SPEED = (70*1.6)*1000/3600 #maximum speed in m/s


class Car:

    def __init__(self, x_axis, y_axis, id,special=False):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.vehicle_speed = np.random.uniform(MIN_SPEED,MAX_SPEED)
        self.accel = np.random.uniform(MIN_ACCELERATION,MAX_ACCELERATION)
        self.special = special
        self.id =id


    """####################################################
    Function name: get_coordinates
    Description: get the X and Y axis coordinates of the car
    Input Parameters: void
    Output parameters: a list containing [x_axis,y_axis]
    #######################################################"""
    def get_coordinates(self):
        return [self.x_axis,self.y_axis]

    """####################################################
    Function name: set_coordinates
    Description: set the X and Y axis coordinates of the car
    Input Parameters: X and Y coordinates
    Output parameters: void
    #######################################################"""
    def set_coordinates(self, x, y):
        self.x_axis = x
        self.y_axis = y



    """####################################################
    Function name: get_coordinates
    Description: update the car coordinates, and speed. If there
    is any car in front the speed of the back vechile needs to be
    less than the speed of the front vehicle
    Input Parameters: front_vehicle(bool) , ds (int) ,
                      front_vehicle_speed (int)
    Output parameters: the new set of coordinates for the car
    #######################################################"""
    def update_car_properties(self,front_vehicle,ds=0,front_vehicle_speed =0):

        #calculate the new position of the vehicle, assume a 100ms granularity
        distance = round(self.vehicle_speed * 100 * pow(10,-3))
        self.y_axis = self.y_axis + distance

        #calculate acceleration, make sure is inside the range
        while True:
            while True:
                random = np.random.uniform(-1,1)
                accel = np.random.uniform(0,5) *random

                ##check the accel to make sure is in range
                if(accel>=MIN_ACCELERATION and accel<=MAX_ACCELERATION):
                    self.accel=accel
                    break

            #see if the car was behind another car, as a result it could have
            #decelerated too much, fix this
            if MIN_SPEED-self.vehicle_speed >0:
                speed = MIN_SPEED
                break
            #calculate the speed of the vehicle , make sure is between range
            speed = round(self.vehicle_speed +  self.accel)

            #break if the speed is between the limit
            if(speed>=MIN_SPEED and speed<=MAX_SPEED ):
                break

        #if the vehicle has a vehicle in front, thus it is inside safety distance
        if front_vehicle==True:
            min_speed = (-BETA + math.sqrt(math.pow(BETA,2)+(4*SIGMA*ds)))/(2*SIGMA)
            self.vehicle_speed = round(min(min_speed,speed))


        #vehicle is not following any vehicle
        else:
            self.vehicle_speed = speed











