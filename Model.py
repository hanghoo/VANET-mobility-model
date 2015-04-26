__author__ = 'muzcategui'
# Filename: Model.py

import numpy as np

from Car import Car


#costants
LANES = 4
DS =10 #meters
TOLERANCE_TIME=0 #second
MIN_SPEED = 50 #meters
MAX_SPEED = 70 #meters
TRAFFIC_VOLUME = 3000 #vehicles/hour/lane
ARR_DEP_RATE = 0.833 # arrival/ departure rate
TRAFFIC_DENSITY_MIN = 100 # minimum traffic density per lane
TRAFFIC_DENSITY_MAX = 500 # maximum traffic density per lane

#variable
num_cars_lane1 = 100
num_cars_lane2 = 100
num_cars_lane3 = 100
num_cars_lane4 = 100
model_cars = []
lanes_cars_num = [0,0,0,0]

def start_model():
    for i in range(LANES):
        positions = []
        lane = 4 +(i*3) #lane position, the + 4 is the offset from the y axis
        for j in range(TRAFFIC_DENSITY_MIN):
            # generate the car position
            while True:
                y_axis = np.random.uniform(0,5000)

                #make sure psoition of two cars dont overlap
                if  not positions.__contains__(y_axis):
                    positions.append(y_axis)
                    break
            car = Car(lane,y_axis)
            model_cars.append(car)
            #add car to the lane
            lanes_cars_num[i]+=1
            print('h')










