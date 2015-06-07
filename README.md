# VANET-mobility-model

The project demonstrates the effectiveness of VANET as the future of vehicular networking. 
The project is composed of two parts - the first part shows the communication properties between VANET neighbors, 
such as average number of neighbors at different lane densities, the number of neighbors a car can maintain and for how long and 
the second part demonstrates V2I and V2V communications graphically. The simulations were developed using python 3 along with matplotlib, numpy and scipy modules.


## Running the Code:

## Part I:
1. Make sure the Car.py and Model.py files are in the same folder.
2. To start running the code, you can use the command “python3 Model.py” on the terminal.
3. Before the code starts running, the user will be asked to select a communication range (50m or 100m), and the number
of iterations that the user desires. Note that the each iteration accounts for a 100ms of vehicular simulation, if ten minutes are desired, the user should input 6000 iterations. Then the code will execute 10 minutes of simulation 5 times.

## Part II (V2V Communication):
1. To simulate the V2V communication, run the file Model_2.py using the command “python3 Model_2.py”.
2. When the grid is shown, place 2 points to create the first line (road). Then place 2 more points to create the second line (road). Make sure the second line intersects the first line.
3. After the 2 lines are drawn, the simulation starts with 3 cars. When the cars are within 100m of each other, a connection (green line) is shown between these cars indicating that they are in communication range.

## Part II (V2I Communication):
1. To simulate the V2I communication, run the file Model_2.2.py using the command “python3 Model_2.2.py”.
2. The user is asked to select the number of Road Side Units (RSUs). The number of RSUs can be between 1 and 3.
3. Once the number of RSUs is entered, the grid will show up. Place 5 points on the grid to create a path representing 4 roads.
4. After the path is drawn, place the required number of points indicating the number of RSUs.
5. Then a car will start moving on the path and when it reaches 100m within any RSU, a connection (green line) is shown between the car and that RSU indicating that the car is within the communication range of
that RSU. The path where the car is within the communication range of an RSU is highlighted in green.
