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

    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.vehicle_speed = np.random.uniform(MIN_SPEED,MAX_SPEED)
        self.accel = np.random.uniform(MIN_ACCELERATION,MAX_ACCELERATION)


    """####################################################
    Function name: get_coordinates
    Description: get the X and Y axis coordinates of the car
    Input Parameters: void
    Output parameters: a list containing [x_axis,y_axis]
    #######################################################"""
    def get_coordinates(self):
        return [self.x_axis,self.y_axis]

    """####################################################
    Function name: get_speed
    Description: get the speed of the vehicle
    Input Parameters: void
    Output parameters: speed of the vehicle in m/s
    #######################################################"""
    def get_speed(self):
        return self.vehicle_speed

    """####################################################
    Function name: get_accel
    Description: get the acceleration of the vehicle
    Input Parameters: void
    Output parameters: acceleratio  of the vehicle in m/s^2
    #######################################################"""
    def get_accel(self):
        return self.accel


    """####################################################
    Function name: get_coordinates
    Description: update the car coordinates, and speed. If there
    is any car in front the speed of the back vechile needs to be
    less than the speed of the front vehicle
    Input Parameters: front_vehicle(bool) , ds (int) ,
                      front_vehicle_speed (int)
    Output parameters: void
    #######################################################"""
    def update_car_properties(self,front_vehicle,ds=0,front_vehicle_speed =0):

        #calculate the new position of the vehicle, assume a 100ms granularity
        distance = round(self.vehicle_speed * 100)
        self.y_axis = self.y_axis + distance

        #calculate acceleration, make sure is inside the range
        while True:
            random = np.random.uniform(-1,1)
            self.accel = random * self.accel

            ##check the accel to make sure is in range
            if(self.accel>=MIN_ACCELERATION and self.accel<=MAX_ACCELERATION):
                break

        #calculate the speed of the vehicle , make sure is between range
        while True:
            speed = self.vehicle_speed + random * self.accel
            if(speed>=MIN_SPEED and speed<=MAX_SPEED ):
                break

            #if the vehicle has a vehicle in front, thus it is inside safety distance
            if front_vehicle==True:
                while True:
                    min_speed = (-BETA + math.sqrt(math.pow(BETA,2)+(4*SIGMA*ds)))/(2*SIGMA)

                    #if the min_ speed is not inside the speed range, disregard the calculation
                    if(min_speed<MIN_SPEED):
                        min_speed = MAX_SPEED
                self.vehicle_speed = min(min_speed,speed)
            else:
                self.vehicle_speed = speed











