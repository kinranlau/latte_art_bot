#%%
'''
This function creates actions to shake the jug.
This is achieved by quickly stopping by 4 points (±x, ±y) of a circle.
    Parameters:
            filename (str): the txt file to read the last position
            shake_filename (str): the txt file to be saved
            shake_radius (float): defines the radius (magnitude) of shaking (in cm)
            shake_speed_num (int): controls the speed of shaking, 1 is the fastest, >1 will be slower
            shake_num (int): number of times to shake the jug, one time is one circle
            clockwise (bool): True: clockwise shaking; False: anticlockwise shaking

    Returns:
            shake_filename.txt: txt file containing the actions to shake the jug
'''
#%%
import numpy as np
import tinyik

#%%
# read current servo positions from txt file
filename = '6_pre_shake_easeinout10.txt'
# save new servo positions as txt file
shake_filename = '7_shake_jug.txt'
# shake radius (cm)
shake_radius = 2.5
# shake speed controlled by staying at the same coordinate for n number of steps
shake_speed_num = 1
# shake number of times
shake_num = 5
# clockwise or anticlockwise
clockwise = True

#%%
# read current servo positions from txt file
# open file
file = open(filename, "r")
data=file.read()
saved_positions=eval(data)

last_position = saved_positions[-1]
file.close()

# we only use the first 3 servos for forward/inverse kinematics here
servo1 = last_position[0]
servo2 = last_position[1]
servo3 = last_position[2]
# negative servo2 and servo3 correcting for rotation orientation
servo_3angles = [servo1, -servo2, -servo3]

#%%
# define robot geometry for forward and inverse kinematics
# have to be careful how you define your axes in the first place

# joint angles are zero by default, define actuator rotation axes and length accordingly
# 1R: rotation along z axis, a short link of 1.5 cm in the z direction
# 2R: rotation along x axis, a link of -9.6 cm in the y direction
# 3R: rotation along x axis, a link of -17.7 cm in the y direction
robot = tinyik.Actuator(['z', [0., 0., 1.5], 'x', [0., -9.6, 0.], 'x', [0., -17.7, 0.]])

# initialise angles of the fisrt 3 joints
# because we only use the first 3 joints to calculate the final coordinates
robot.angles = np.deg2rad(servo_3angles)

# use forward kinematics to get the initial coordiantes
coordinates = np.round(robot.ee, decimals = 1)

#%%
# create a shaking action by quickly stopping by 4 points (±x, ±y) of a circle with a `shake_radius`

# get new coordinates when shaking the jug with a specified shake radius
minus_x = coordinates - np.array([shake_radius, 0, 0]) 
plus_y = coordinates + np.array([0, shake_radius, 0]) 
plus_x = coordinates + np.array([shake_radius, 0, 0]) 
minus_y = coordinates - np.array([0, shake_radius, 0]) 

# clockwise or anticlockwise shaking
if clockwise == True:
    new_coordinates = [minus_x, plus_y, plus_x, minus_y]
else:
    new_coordinates = [plus_x, plus_y, minus_x, minus_y]
    
new_servo = []

# use inverse kinematics to get the respective servo positions
for coordinate in new_coordinates:
    # set new coordinates
    robot.ee = coordinate
    # use inverse kinematics to get new servo positions
    servo_3angles = np.round(np.rad2deg(robot.angles))
    # negative servo2 and servo3 correcting for rotation orientation
    servo_3angles = np.multiply(servo_3angles, [1, -1, -1])

    # append servo positions to list
    for i in range(shake_speed_num):
        new_servo.append(servo_3angles)

#%%
# convert array to list, and add servo 4/5/6 angles back (which were not modified)
new_servo_list = []
new_servo_temp = []

for servo in new_servo:
    servo = servo.astype(int).tolist()
    servo += last_position[-3:]

    new_servo_temp.append(servo)

for i in range(shake_num):
    new_servo_list.extend(new_servo_temp)

# save to txt file
with open(shake_filename, 'w') as f:
    f.write(str(new_servo_list))