from pylab import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import *
from pylab import ginput as input
import numpy as np
import random

#variables
COM_RANGE =100 # communication range of 100m
fig = plt.figure()
ax = fig.add_subplot(111)
scatter = 0
com_lines =[]
line1 = [] # the first line
line2 = [] # the second line
cars ={}
time_per_iteraiton = 100*math.pow(10,-3)

#grpahs parameters
ax.set_ylim([0,1000])   # setting the grid length to 5 units (assume 1 unit = 1mile)
ax.set_xlim([0,1000])  # Generate 4 lanes with distance between each as 3 units
ax.set_xlabel('meters')
ax.set_ylabel('meters')
ax.grid(True)


"""####################################################
Function name: get_line()
Description: Get all the points in a line
Input Parameters: void
Return parameters: list of points in the line
#######################################################"""
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


"""####################################################
Function name: display_grid()
Description: display the grid that will be used by the user
             it allows the user to create an intersection
Input Parameters: void
Output parameters: void
#######################################################"""
def display_grid():
    #define global variables

    #get the first line and plot it
    global line1
    points1 = input(2) # get the 2 end points of the line
    x1= [x[0] for x in points1]
    y1=[x[1] for x in points1]
    points1 = get_line(int(x1[0]),int(y1[0]),int(x1[1]),int(y1[1])) # Get all the points in the line
    x1= [x[0] for x in points1]
    y1=[x[1] for x in points1]
    line1 = plt.Line2D(x1,y1) # Create a line object with the x y values of the points in a line
    plt.gca().add_line(line1)
    plt.draw()


    #get the second line and plot it
    global line2
    points2 = input(2) # get the 2 end points of the line
    x2= [x[0] for x in points2]
    y2=[x[1] for x in points2]
    points2 = get_line(int(x2[0]),int(y2[0]),int(x2[1]),int(y2[1])) # Get all the points in the line
    x2= [x[0] for x in points2]
    y2= [x[1] for x in points2]
    line2 = plt.Line2D(x2,y2,label='road') # Create a line object with the x y values of the points in a line
    plt.gca().add_line(line2)
    plt.draw()
    

"""####################################################
Function name: display_cars()
Description: display the cars in a graph
Input Parameters: void
Output parameters: void
#######################################################"""
def display_cars():
    #define global variables
    global scatter
    global cars

    #temporal variable to hold values of cars
    points = [[],[]]
    car_lines = [line1,line1,line2]

    #get 3 cars in the graph
    for i in range(3):
        #pick the line of the car from the previously created
        # line of cars, so that car1 gets line1 car2 gets line1
        #and car3 gets line1
        car_line = car_lines[i]
        point = car_line.get_xydata()[0] #first point in the graph

        #calculate the angle
        line_data= car_line.get_data()
        xdiff = line_data[0][-1]-line_data[0][0]
        ydiff = line_data[1][-1]-line_data[1][0]
        ang = atan2(ydiff,xdiff)
        #for the second car shift angle to negative
        #so that it goes in opposite direction from car1
        if i==1:
            ang = ang + math.pi
            point = car_line.get_xydata()[-1] #for this car get the last point as positions

        #get the minimum and maximums of the line to include
        # as a car property
        x_min = min(line_data[0])
        x_max = max(line_data[0])

        #add all the properties to the car
        temp = []
        temp.append(point[0])
        temp.append(point[1])
        temp.append(ang)
        temp.append(x_min)
        temp.append(x_max)

        cars[i]= temp   # Create an array of all the cars

        #add scatter
        points[0].append(point[0])
        points[1].append(point[1])

    #plot the cars
    scatter = plt.scatter(points[0],points[1], color = 'red', marker = 's',label = 'cars')
    plt.legend(handles=[scatter,line2],loc='upper center', shadow=True)
    plt.draw()


'''############################################################################################
Function name: simulate_car_movement()
Description: Simulate the car movements in the given path.
             Visualize the communication between the cars when they are in communication range
Input Parameters: scatter and empty list of communication lines
Return parameters: scatter, com_lines
################################################################################################'''
def simulate_car_movement(scatter,com_lines):
    #temporal variables
    points= [[],[]]
    cars_to_delete = []
    scatter.remove()


    while com_lines:
        com_lines[0].remove()
        del(com_lines[0])


    #iterate over each car
    for car in cars:
        #get all the properties of the car
        velocity = round(np.random.uniform(10,20))
        position_x = cars[car][0]
        position_y = cars[car][1]
        angle = cars[car][2]

        #calculate new position of the car
        position_x =position_x + velocity*cos(angle)*time_per_iteraiton
        position_y = position_y + velocity*sin(angle)*time_per_iteraiton
        #check if car gets out of the line
        # no need to check for y coordinates as car follows the line
        if position_x < cars[car][3] or position_x> cars[car][4]:
            cars_to_delete.append(car)
        else:
            cars[car][0]=position_x
            cars[car][1]=position_y
            points[0].append(position_x)
            points[1].append(position_y)

            #check if the car is communicating with other vehicles
            for key in cars:
                #skip the iteration if we are looking at the same car
                if cars[key] == cars[car]:
                    continue
                else:
                    #compute to see if vehicle is in range
                    inside = math.pow((cars[key][0]-position_x),2) + math.pow((cars[key][1]-position_y),2)
                    if inside <= math.pow(COM_RANGE,2):
                        line = plt.Line2D([position_x,cars[key][0]],[position_y,cars[key][1]],color='green')

                        com_lines.append(line)
                        plt.gca().add_line(line)


    #delete the cars  out of the dictionary
    for i  in cars_to_delete:
        del(cars[i])

    #update the scatter and plot
    scatter = plt.scatter(points[0],points[1], color = 'red', marker = 's')
    plt.draw()

    return [scatter,com_lines]



display_grid()
display_cars()
i =0
while cars:
   [scatter,com_lines] = simulate_car_movement(scatter,com_lines)

plt.show()
