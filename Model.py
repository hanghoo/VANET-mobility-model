import matplotlib.pyplot as plt
from pylab import *
import numpy as np # for the entry cars
import numpy as np1 # for the exit of cars
import random
from Car import Car

#constants
DS =10 #meters
TOLERANCE_TIME=0 #second
ARR_DEP_RATE = 0.833 # arrival/ departure rate
TRAFFIC_DENSITY_MIN = 0 # minimum traffic density per lane, it will be assigned a value for every
                        # iteration of the main loopp
TRAFFIC_DENSITY_MAX = 500 # maximum traffic density per lane
LANE_SEPARATION =3 #lane separation is 3 meters
COM_RANGE = 0   #Input by user to use through the simulation
COM_TIME_SAME_NEIGHBORS =100 #constant to check for communication time, it is set to 10seconds seconds, value could raneg [100,600]
NUM_ITERATIONS = 0

#variables
lane1_car_positions = [] #holds all the positions in lane 1
lane2_car_positions =[] #holds all the positions in lane 2
lane3_car_positions = [] #holds all the positions in lane 3
lane4_car_positions = [] #holds all the positions in lane 4
lane1_cars= [] #holds all the car objects in lane 1
lane2_cars = []  #holds all the car objects in lane 2
lane3_cars =[] #holds all the car objects in lane 3
lane4_cars =[] #holds all the car objects in lane 4
car_positions_in_each_lane = [lane1_car_positions, lane2_car_positions, lane3_car_positions, lane4_car_positions]   # Lists of cars' positions in their respective lanes.
cars_in_all_lanes = [lane1_cars, lane2_cars, lane3_cars, lane4_cars]        # Lists of all the car objects present in all the 4 lanes
target_car_position = [] # the position fo the target car
id =0




"""####################################################
Function name: start_model
Source: StackOverflow
Description: start the model by distributing 100 cars
             per lane randomly but uniformly
Input Parameters: the initial plot of the model
Output parameters: a list containing a list of all the vehicle positions
#######################################################"""
def start_model():
    global target_car_position
    global id
    global car_positions_in_each_lane
    global cars_in_all_lanes


    #add a 100 car per lane uniformly distributed randomly
    for i in range(len(car_positions_in_each_lane)):
        lane = 2 +(i*3)
        for j in range(TRAFFIC_DENSITY_MIN):
            # generate the car position
            while True:
                y_axis =round(np.random.uniform(0,5000))

                #make sure psoition of two cars dont overlap
                if  not  y_axis in car_positions_in_each_lane[i]:
                    break
            car_positions_in_each_lane[i].append(y_axis)
            car = Car(lane,y_axis,id)
            id+=1
            cars_in_all_lanes[i].append(car)

    # add the target car in a random lane in a random position
    while True:
        lane = random.choice([0,1,2,3])
        y_axis = round(np.random.uniform(0,5000))
        lane_axis = 2 +(lane*3)
        target_car_position =[lane_axis,y_axis]


        #check that no car is in that position already
        if not y_axis in car_positions_in_each_lane[lane]:
            cars_in_all_lanes[lane].append(Car(lane_axis,y_axis,id,True))
            id+=1
            car_positions_in_each_lane[lane].append(y_axis)
            break




"""####################################################
Function name: entry_exit_vehicle()
Description: Determines if a vehicle needs to enter or exit the rode
Input Parameters: number of iteration to get the value of the exponential
                  random number
Output parameters: void
#######################################################"""
def entry_exit_vehicle(iteration):
    global id
    global target_car_position
    #determine if a vehicle is to enter a lane
    for i in range(len(car_positions_in_each_lane)):
        lane = 2 + (i*3)
        rand = np.mean(np.random.exponential(1,iteration+1))
        #dont add a car if the lane is full
        if len(car_positions_in_each_lane[i]) < TRAFFIC_DENSITY_MAX:
            if rand < ARR_DEP_RATE:
                #choose at random the ramp position
                ramp = random.choice([1500,2500,4000])
                if not ramp in car_positions_in_each_lane[i]:
                    cars_in_all_lanes[i].append(Car(lane,ramp,id))
                    id+=1
                    car_positions_in_each_lane[i].append(ramp)


        #determine if a vehicle is to exit
        #determine if a vehicle needs to exit the lane
        iterator = [1550,2550,4050] #the ramp positions
        if len(car_positions_in_each_lane[i]) > TRAFFIC_DENSITY_MIN:
            for j in iterator:
                #check that a car is in position to exit
                if j in car_positions_in_each_lane[i]:
                    #decide whether the car will exit or not
                    rand = np1.mean(np1.random.exponential(1,iteration+1))
                    if rand <  ARR_DEP_RATE:
                        #get the index
                        index = car_positions_in_each_lane[i].index(j)
                        #check that it is not the target car
                        if cars_in_all_lanes[i][index].special == False :
                            car_positions_in_each_lane[i].remove(car_positions_in_each_lane[i][index])
                            car = cars_in_all_lanes[i][index]
                            cars_in_all_lanes[i].remove(cars_in_all_lanes[i][index])
                            del(car)


"""####################################################
Function name: update_model
Description: updates the position and speed of every vehicle
             in the model, it performs the freeway mobility,
             the car following, and lane changing behavior models
Input Parameters: void
Output parameters: returns a list containing three values, the average
                    number of neighbors, the average time
                    that the car kept three neighbors, and the average number of
                    neighbors the car manages to mantain for 10 seconds
#######################################################"""
def update_model():

    global target_car_position
    global id

    cars_neighbors = [] #list containing sublists of car neighbors for every 100ms

    #do five iterations of 10 minutes of vehicular mobility
    # each iteration at a 100 ms granularity
    for i in range(5):
        #simulate ten minutes
        for j in range(NUM_ITERATIONS):
            if j % 10 ==0:  #to do the entry / exit every second instead of milisecond
                entry_exit_vehicle((i*600)+j)
            cars_neighbors_100ms=[]
            # update the cars per lane
            #simulate a second at 100ms granularity
            for k in range(len(cars_in_all_lanes)):
                for m in range(len(cars_in_all_lanes[k])):
                    #get the y axis position of that car
                    # get the car coordinates of the car and
                    #create a set of invalid coordinates for the next car
                    try:
                        coordinates =cars_in_all_lanes[k][m].get_coordinates()
                        l = list(range(round(coordinates[1])+1,round(coordinates[1])+DS)) #list of invalid car positions
                    except IndexError:
                        break #since we are deleting an arrayu dinamically, make sure we do not get out of range

                    #check whether the car is following a front car or not
                    cars_in_front =list(set(car_positions_in_each_lane[k]) & set (l))
                    if not cars_in_front :
                        cars_in_all_lanes[k][m].update_car_properties(False)
                        #update the positions in the lane list
                        car_positions_in_each_lane[k][m]=cars_in_all_lanes[k][m].y_axis
                    else:
                        same_lane = not lane_change(k,m,car_positions_in_each_lane[k][m])
                        if same_lane == False:
                            m -=1
                            if m <= 0:
                                m = 0
                            continue
                        cars_in_all_lanes[k][m].update_car_properties(True,min(cars_in_front)-coordinates[1])
                        car_positions_in_each_lane[k][m]=cars_in_all_lanes[k][m].y_axis

                    #get coordinates if the car is the target car
                    if cars_in_all_lanes[k][m].special == True:
                        target_car_position= cars_in_all_lanes[k][m].get_coordinates()


                    #check if the car got out of range
                    if cars_in_all_lanes[k][m].y_axis >5000:
                        target = cars_in_all_lanes[k][m].special

                        #delete the car
                        car =cars_in_all_lanes[k][m]
                        cars_in_all_lanes[k].remove(cars_in_all_lanes[k][m])
                        car_positions_in_each_lane[k].remove(car_positions_in_each_lane[k][m])
                        del(car)
                        #reduce index to avoid iterating out of index
                        m -=1
                        if m <0:
                            m = 0

                        #add a new car in a random position that has not been taken yet, or
                        #if the density is already at minimun, remove the car and added in the same lane
                        #choose lane
                        if len(cars_in_all_lanes[k]) ==TRAFFIC_DENSITY_MIN:
                            lane = k
                        else:
                            lane = random.choice([0,1,2,3])

                        #choose at random the ramp position
                        temp_list = set(range(0,5000))
                        pos =car_positions_in_each_lane[lane]
                        entry_position = random.choice(list(temp_list.difference(pos)))
                        cars_in_all_lanes[lane].append(Car(2+(lane*3),entry_position,id,target))
                        if target ==True:
                            target_car_position = [2+(lane*LANE_SEPARATION),entry_position]
                        id+=1
                        car_positions_in_each_lane[lane].append(entry_position)
                        continue

                    #check if vehicle is inside of target
                    if cars_in_all_lanes[k][m].special == False:
                        inside = math.pow((cars_in_all_lanes[k][m].x_axis -target_car_position[0]),2) + \
                                 math.pow((cars_in_all_lanes[k][m].y_axis -target_car_position[1]),2)
                        if inside <= math.pow(COM_RANGE,2):
                             cars_neighbors_100ms.append(cars_in_all_lanes[k][m].id)
            cars_neighbors.append(cars_neighbors_100ms)


    return get_com_neighbor_info(cars_neighbors)





"""######################################################################
Function name: lane_change()
Description: The vehicle can change lanes, but it has to make sure there
             is no vehicle within the safety distance of the new position
             in the chosen adjacent lane.
#######################################################################"""
def lane_change(i,j,car_pos):
    is_car_within_safety_distance = False               #Is there a car in the neighbouring lane within the saftey distance
    lane_to_move_to = 0
    possible_lanes = []

    if i==0 or i==3:

        if i == 0:
            lane_to_move_to = 1
        elif i == 3:
            lane_to_move_to = 2


        ##########################################################
        # Change limits 1 and 3 to 100 and 500 after testing
        ##########################################################
        if len(car_positions_in_each_lane[i]) <= TRAFFIC_DENSITY_MIN or len(car_positions_in_each_lane[lane_to_move_to]) >= TRAFFIC_DENSITY_MAX:
            # If number of cars in current lane is less than 100 or number of cars in next lane is more than 500, then don't change lane.
            return False

        points_within_safety_distance = list(range(car_pos-10,car_pos+11))  # List of points which is within 10m of the car in the current lane.

        for k in car_positions_in_each_lane[lane_to_move_to]:           # Get positions of all cars in lane_to_move_to
            # Check if any point in lane_to_move_to is present within 10m distance of car in current lane, i.e,
            # check if car from current lane can move to lane_to_move_to and there are no cars within safety distance in lane_to_move_to
            if k in points_within_safety_distance:
                is_car_within_safety_distance = True        # There is a car within the safety distance
                break
            else:
                is_car_within_safety_distance = False       # There is no car within the safety distance

        if (is_car_within_safety_distance == False):
            # No car withing saftety distance in next lane. Hence move the car to next lane.
            move_car_to_next_lane(lane_to_move_to, car_pos, i, j)
            return True
        else:
            # There is car within the saftey distance in next lane. Hence, don't change lane.
            return False


    elif i == 1 or i == 2:
        possible_lanes = [i-1,i+1]                          # For lanes 1 and 2, there are 2 lane options for the car.
        lane_to_move_to = random.choice(possible_lanes)     # i+2, so that we even have the i+1 lane to choose from. If we have (i-1,i+1), the i+1 lane will never be chosen as its excluded.

        if len(car_positions_in_each_lane[i]) <= TRAFFIC_DENSITY_MIN:
            #If number of cars in current lane is less than 100, then don't change lane.
            return False

        n = 0
        points_within_safety_distance = list(range(car_pos-10,car_pos+11))  # List of points which is within 10m of the car in the current lane.

        while n < 2:
            is_car_within_safety_distance = False                           # Reset the value to false. Required when 1st lane change option doesn't happen.

            for k in car_positions_in_each_lane[lane_to_move_to]:           # Get positions of all cars in lane_to_move_to
                # Check if any point in lane_to_move_to is present within 10m distance of car in current lane, i.e,
                # check if car from current lane can move to lane_to_move_to and there are no cars within safety distance in lane_to_move_to
                if k in points_within_safety_distance:
                    is_car_within_safety_distance = True        # There is a car within the safety distance
                    break
                else:
                    is_car_within_safety_distance = False

            if len(car_positions_in_each_lane[lane_to_move_to]) >= TRAFFIC_DENSITY_MAX:
                #If number of cars in current lane is more than 500, then don't change lane.
                is_car_within_safety_distance = True

            if is_car_within_safety_distance == True:
                n = n+1
            else:
                n = 2

            if ( n < 2 and is_car_within_safety_distance == True):
                # Try moving the car to another lane, if current option didn't work out.
                possible_lanes.remove(lane_to_move_to)              # Remove the lane which cannot be moved to from the list of possible_lanes
                lane_to_move_to = possible_lanes[0]                 # Try with the other lane left in the possible_lanes list


        if (is_car_within_safety_distance == False):
            # No car withing saftety distance in next lane. Hence move the car to next lane.
            move_car_to_next_lane(lane_to_move_to, car_pos, i, j)
            return True
        else:
            return False

"""##############################################################################
Function name: move_car_to_next_lane()
Description: Add the current car object to the list of car objects of next lane
             and remove from current list. Add the position of current car to the
             list of positions of cars in next lane and remove it from current list.
#################################################################################"""
def move_car_to_next_lane(lane_to_move_to, car_pos, i, j):
    global car_positions_in_each_lane
    global car_in_all_lanes
    global id
    # There is a no car within the safety distance in lane_to_move_to. Hence car from current lane can move to lane_to_move_to
    car_positions_in_each_lane[lane_to_move_to].append(car_pos)                                     # Add the car position to list of the next lane car positions.
    cars_in_all_lanes[i][j].set_coordinates((2+(LANE_SEPARATION*lane_to_move_to)), car_pos)                       # Set the x coordinate to the new lane x value.
    cars_in_all_lanes[lane_to_move_to].append(cars_in_all_lanes[i][j])                           # Add the current car object to the list of car objects of next lane
    cars_in_all_lanes[i].remove(cars_in_all_lanes[i][j])
    car_positions_in_each_lane[i].remove(car_pos)                                                   # Remove the car from the current lane.

"""######################################################################
Function name: get_com_neighbor_info
Description: calculates the average number of neighbors, the average time
             that the car kept three neighbors, and the average number of
             neighbors the car manages to mantain for 10 seconds
input parameter: neighbors_100ms (list of list, where each list contains the
                                 ids that the target is associated for 100ms)
outpiut parameters = [avg_num_neighbors,same_3_neighbors_count,same_neighbors_count]
#######################################################################"""
def get_com_neighbor_info(neighbors_100ms):
    num_neighbors=[]
    same_3_neighbors = sorted(neighbors_100ms[0])
    same_3_neighbors_time =0
    same_3_neighbors_times=[]
    same_3_neighbors_count =0
    same_neighbors = sorted(neighbors_100ms[0])
    same_neighbors_time =0
    same_neighbors_lengths=[]
    same_neighbors_count =0

    #1 Iterate over each element
    for i in range(len(neighbors_100ms)):
        # 2 append to get the average of neighbors at the end
        current =neighbors_100ms[i]
        current_length = len(current)
        num_neighbors.append(current_length)
        #3 make sure we do not get out of range
        try:
            next =neighbors_100ms[i+1]
        except IndexError:
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
            if same_neighbors_time> COM_TIME_SAME_NEIGHBORS:
                same_neighbors_lengths.append(len(same_neighbors))
            break

        #if the current set is empty, means no neighbors,
        #initialize all the counters
        if not current:
            same_3_neighbors=sorted(set(next))
            #add to the list of count for 3 same_neighbors
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
            same_3_neighbors_time=0
            same_neighbors= sorted(set(next))
            same_neighbors_time=0
            continue

        # 3 sort both lists to avoid errors
        #3.1 before sorting, make sure there is something
        sorted(current)
        sorted(next)

        #4 check for how much time the car had at the same 3 com neighbors or more
        if len(set(same_3_neighbors) & set(next)) >=3:
            same_3_neighbors_time+=1
            same_3_neighbors= sorted(set(same_3_neighbors) & set(next))
        else:

            #add to the list of count for 3 same_neighbors
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
                same_3_neighbors_time=0

        #5 check that the communication
        if set(same_neighbors).issubset(set(next)) :
            #5.1 make sure is for the specified time
            # the default is 10 seconds, change variable COM_TIME_SAME_NEIGHBORS
            same_neighbors_time+=1
            if same_neighbors_time> COM_TIME_SAME_NEIGHBORS:
                same_neighbors_lengths.append(len(same_neighbors))
                same_neighbors_time =0
        #5.1 if the neighbors are not the same, reset
        else:
            same_neighbors= next
            same_neighbors_time=0
    avg_num_neighbors = round(np.mean(num_neighbors))
    if same_3_neighbors_times:
       same_3_neighbors_count = round(np.mean(same_3_neighbors_times)*100) #to get in ms
    if same_neighbors_lengths:
        same_neighbors_count = round(np.mean(same_neighbors_lengths))

    print([avg_num_neighbors,same_3_neighbors_count,same_neighbors_count])

    return [avg_num_neighbors,same_3_neighbors_count,same_neighbors_count]

"""######################################################################
Function name: reset_model()
Description: reset all the main parameters of the model
returns: void
#######################################################################"""
def reset_model():
    global target_car_position
    global id
    global car_positions_in_each_lane
    global cars_in_all_lanes
    global lane1_car_positions,lane2_car_positions, lane3_car_positions, lane4_car_positions
    global lane1_cars ,lane2_cars ,lane3_cars ,lane4_cars

    #empty all the variables
    lane1_car_positions = []
    lane2_car_positions =[]
    lane3_car_positions = []
    lane4_car_positions = []
    lane1_cars= []
    lane2_cars = []
    lane3_cars =[]
    lane4_cars =[]
    car_positions_in_each_lane = [lane1_car_positions, lane2_car_positions, lane3_car_positions, lane4_car_positions]   # Lists of cars' positions in their respective lanes.
    cars_in_all_lanes = [lane1_cars, lane2_cars, lane3_cars, lane4_cars]        # Lists of all the car objects present in all the 4 lanes
    target_car_position = [] # the position fo the target car
    id =0




"""######################################################################
Description: main executable code
#######################################################################"""
#set the list of minimum traffic densities to be used for this simulation
traffic_densities = list(range(100,550,50))

num_neighbors = [] #average number of neighbors
time_3_neighbors =[] #time that target car mantained the same three communication neighbors
same_neighbors = [] #num of neighbors the target manatined for 10 seconds
fig1 = plt.figure(1)
fig2 = plt.figure(2)
fig3 = plt.figure(3)
ax1 = fig1.add_subplot(111)
ax2 = fig2.add_subplot(111)
ax3 = fig3.add_subplot(111)

#setup the axes
ax1.grid(True)
ax1.set_xlim([0,550])
ax1.ticklabel_format(useOffset=False)
ax2.grid(True)
ax2.ticklabel_format(useOffset=False)
ax2.set_xlim([0,550])
ax3.grid(True)
ax3.set_xlim([0,550])
ax3.ticklabel_format(useOffset=False)

#ask or the desired communication range
COM_RANGE = int(input('Enter the communication range: '))
NUM_ITERATIONS = int(input('Enter the number of 100ms iterations desired: '))

#do the model simulation for every traffic density
for i in traffic_densities:
    #adjust the traffic density to change per iteration
    TRAFFIC_DENSITY_MIN = i
    #reset the global variables, restart the model
    #get the results for specific traffic density
    reset_model()
    start_model()
    results=update_model()
    num_neighbors.append(results[0])
    time_3_neighbors.append(results[1])
    same_neighbors.append(results[2])


# plot the results in different graphs
ax1.set_title('Average number of VANET neighbors')
ax1.set_xlabel('traffic density per lane')
ax1.set_ylabel('vehicles')
ax1.scatter(traffic_densities,num_neighbors)
ax1.plot(traffic_densities,num_neighbors ,label='number of neighbors')
legend = ax1.legend(loc='upper center', shadow=True)


ax2.set_title('Average time with at least 3 same neighbors')
ax2.set_xlabel('traffic density per lane')
ax2.set_ylabel('Time (ms)')
ax2.scatter(traffic_densities,time_3_neighbors)
ax2.plot(traffic_densities,time_3_neighbors,label='time with at least same three neighbors')
legend = ax2.legend(loc='upper center', shadow=True)

ax3.set_title('Same communication neighbors the target have for 10 seconds')
ax3.set_xlabel('traffic density per lane')
ax3.set_ylabel('vehicles')
ax3.scatter(traffic_densities,same_neighbors)
ax3.plot(traffic_densities,same_neighbors, label='number of same com neighbors for 10 seconds')
legend = ax3.legend(loc='upper center', shadow=True)

#show the plot
plt.show()





























