import matplotlib.pyplot as pl
from pylab import *
import numpy as np
import random

figure(0)
pl.ylim([0,5000])   # setting the grid length to 5 units (assume 1 unit = 1mile)
pl.xlim([0,12])  # Generate 4 lanes with distance between each as 3 units


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
    pl.show()



entry_ramp_positions = generate_entry_ramp_positions()
print(entry_ramp_positions)
plot_grid(entry_ramp_positions)






