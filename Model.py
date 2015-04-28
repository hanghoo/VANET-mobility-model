import matplotlib.pyplot as pl
from pylab import *
import numpy as np
import random
from Car import Car

#constants
LANES = 4
DS =10 #meters
TOLERANCE_TIME=0 #second
MIN_SPEED = 50 #meters/s
MAX_SPEED = 70 #meters/s
TRAFFIC_VOLUME = 3000 #vehicles/hour/lane
ARR_DEP_RATE = 0.833 # arrival/ departure rate
TRAFFIC_DENSITY_MIN = 100 # minimum traffic density per lane
TRAFFIC_DENSITY_MAX = 500 # maximum traffic density per lane
figure(0)
pl.ylim([0,5000])   # setting the grid length to 5 units (assume 1 unit = 1mile)
pl.xlim([0,12])  # Generate 4 lanes with distance between each as 3 units

#variables
model_cars = []
lanes_cars_num = [0,0,0,0]


'''########################################################################
# Function name: generate_entry_ramp_positions
# Description: Generate entry ramp positions randomly. Make sure that the
# values of the positions are not same for any of the 3 ramps.
# Return value: list of postions of entry ramps
###########################################################################'''
def generate_entry_ramp_positions():
    entry_ramp_pos = []

    while (len(entry_ramp_pos) < 3): #Keep trying to generate till we have 3 unique ramp positions.
        temp_position = random.randrange(1, 5000)
        if (len(entry_ramp_pos) == 0): 
            entry_ramp_pos.append(temp_position)    # Generate the first ramp

        else: 
            for j in range(0,len(entry_ramp_pos)):
                if(math.fabs(temp_position-entry_ramp_pos[j]) == 0): 
                    break            # Break out of the loop and dont add this position to the list of ramp position values as its repeatitive

            else:                    # Execute this block if there is no repetitions of ramp position values.
                if(len(entry_ramp_pos) < 3):
                    entry_ramp_pos.append(temp_position)
                    
    return entry_ramp_pos


'''########################################################################
# Function name: plot_grid
# Description: Generate the grid with 4 lanes and 3 exit and entry ramps.
# Input parameters: list of postions of entry ramps 
###########################################################################'''
def plot_grid(entry_ramp_positions):
    
    eventplot([2,5,8,11], orientation='horizontal', lineoffsets=0,linelengths=10000,linewidths=None, color='blue', linestyles='solid')

    # Plot the entery ramp position and then plot the exit ramp 50m units away from the entry ramp
    # Entry and Exit ramp 1
    eventplot([int(entry_ramp_positions[0])], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')
    eventplot([int(entry_ramp_positions[0])+50], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')

    # Entry and Exit ramp 2
    eventplot([int(entry_ramp_positions[1])], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')
    eventplot([int(entry_ramp_positions[1])+50], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')

    # Entry and Exit ramp 3
    eventplot([int(entry_ramp_positions[2])], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')
    eventplot([int(entry_ramp_positions[2])+50], orientation='vertical', lineoffsets=0,linelengths=25,linewidths=None, color='red', linestyles='solid')

    #pl.arrow(6,entry_ramp_positions, 0.5, 0.5, hold=None)
    #pl.annotate("", xy=(0.5, 0.5), xytext=(),arrowprops=dict(arrowstyle="->"))


"""####################################################
Function name: start_model
Description: start the model by distributing 100 cars
             per lane randomly but uniformly
Input Parameters: the initial plot of the model
Output parameters: a list containing a list of all the vehicle positions
#######################################################"""
def start_model():
    model_positions =[]
    for i in range(LANES):
        positions = []
        lane = 2 +(i*3) #lane position, the + 4 is the offset from the y axis
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
            model_positions.append(car.get_coordinates())
            pl.scatter(lane,y_axis,1)

            #add car to the lane
            lanes_cars_num[i]+=1


entry_ramp_positions = generate_entry_ramp_positions()
print(entry_ramp_positions)
plot_grid(entry_ramp_positions)
start_model()
pl.show()









