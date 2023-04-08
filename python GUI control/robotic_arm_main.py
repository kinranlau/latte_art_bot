#%%
'''
This function communicates with arduino and serves the tkinter GUI to control the robot via forward/inverse kinematics.
It can also record and replay actions.
Instructions:
    1. Setting the COM port of arduino:
    The active port (e.g. COM3) can be found in the Device Manager.

    2. Controlling the robot:
    You can control the robot by both forward and inverse kinematics.
    Forward kinematics: change the servo angles, update the x,y,z coordinates.
    Inverse kinematics: change the x,y,z coordinates, update the servo angles.

    The servo angles and x,y,z coordinates are continuously updated.
    You can change the slider values by dragging the sliders, or by using the specified keys on the keyboard.
    (see which keys control which sliders in the code)

    3. Saving actions:
    By clicking `Start saving`, you will start recording the servo angles every 0.1 seconds (the time interval can be changed).
    The servo angles will be saved to the list `saved_positions`.
    To stop the recording, `Change save state` to False.
    If you decide to save the recorded actions as a txt file, you can go to `File` -> `Save File`.

    To record the next series of actions, you need to first `Change save state` to True.
    Then simply `Start saving` again.
    Prior to the next save, you might also want to `Clear All Positions` to remove the actions in the temporary list of `saved_positions`.
    `Clear All Positions` will only clear the temporary list `saved_positions`, and will not affect your saved txt files.

    4. Replaying actions:
    `Replay Positions` will replay the positions in the `saved_positions` list.
    By default, `saved_positions` is an empty list.
    You will first have to record some actions in the list before replaying them.
    Alternatively, you can load the saved actions from a txt file to the `saved_positions` list, which can be done by going to `File` -> `Open File`.

    5. Resetting servos:
    `Reset servos` will reset the servos to the initial positions, which might be helpful before recording another set of actions.
'''
#%%
#######################################
# import libraries
#######################################
import serial
import time

import numpy as np
import tinyik

from tkinter import *
from tkinter import filedialog

import os
path = os.getcwd()

#%%
#######################################
# define parameters and settings
#######################################
# initialise port_opened = False
port_opened=False

# initialise servo angles
servo1 = 90
servo2 = 60
servo3 = 110
servo4 = 90
servo5 = 90
servo6 = 90

# wait time (s)
# increase sleep time to prevent communication error
wait_time = 0.05
# save interval (s)
save_time = 0.1
# play interval (s)
play_time = 0.1

#%%
#######################################
# define robot geometry for forward and inverse kinematics
# have to be careful how you define your axes in the first place
#######################################

# joint angles are zero by default, define actuator rotation axes and length accordingly
# 1R: rotation along z axis, a short link of 1.5 cm in the z direction
# 2R: rotation along x axis, a link of -9.6 cm in the y direction
# 3R: rotation along x axis, a link of -17.7 cm in the y direction
robot = tinyik.Actuator(['z', [0., 0., 1.5], 'x', [0., -9.6, 0.], 'x', [0., -17.7, 0.]])

# initialise angles of the first 3 joints
# because here we only use the first 3 joints for both forward and inverse kinematics
servo_3angles = [servo1, -servo2, -servo3]  # negative servo2 and servo3 correcting for rotation orientation
robot.angles = np.deg2rad(servo_3angles)

# use inverse kinematics to get the initial coordiantes
coordinates = np.round(robot.ee, decimals = 1)

#%%
#######################################
# define all the functions to be called in the GUI
#######################################

#######################################
# set USB port of arduino
#######################################
def set_port():
    global port_opened,arduino
    com_port= port_input.get()
    arduino=serial.Serial(com_port,115200)
    port_opened=True
    print ("COM port set to: "+com_port)

#######################################
# send servo positions to arduino
#######################################
def send_positions(position):
    # the rotation degree is denoted by 3 numbers
    # e.g. '090' for 90 degrees
    # 6 servos in total, so a total of 18 numbers
    message = "{0:0=3d}".format(position[0])+"{0:0=3d}".format(position[1])+"{0:0=3d}".format(position[2])+"{0:0=3d}".format(position[3])+"{0:0=3d}".format(position[4])+"{0:0=3d}".format(position[5])+"\n"
    arduino.write(str.encode(message))
    #print(message, end='')
    # increase sleep time to prevent communication error
    time.sleep(wait_time)

#######################################
# reset servo positions to default values
#######################################
def reset_servos():
    # get default positions
    default_positions = [servo1, servo2, servo3, servo4, servo5, servo6]

    # update the servo sliders with the new positions
    # the new slider values will be sent to arduino automatically in the `while True:` loop 
    servo1_slider.set(default_positions[0])
    servo2_slider.set(default_positions[1])
    servo3_slider.set(default_positions[2])
    servo4_slider.set(default_positions[3])
    servo5_slider.set(default_positions[4])
    servo6_slider.set(default_positions[5])

#######################################
# forward kinematics
# every time when servo1/2/3 move, trigger forward kinematics to calculate the new coordinates
#######################################
def forward_kinematics(angle):
    # negative servo2 and servo3 correcting for rotation orientation
    servo_3angles = [servo1_slider.get(), -servo2_slider.get(), -servo3_slider.get()]

    # set new robot angles
    robot.angles = np.deg2rad(servo_3angles)

    # use forward kinematics to get the new coordiantes
    coordinates = np.round(robot.ee, decimals = 1)

    # set these new coordinates to the x,y,z sliders
    x_slider.set(coordinates[0])
    y_slider.set(coordinates[1])
    z_slider.set(coordinates[2])

#######################################
# inverse kinematcs
# every time x/y/z coordinates change, trigger inverse kinematics to calculate the new servo positions
#######################################
def inverse_kinematics(coor):
    # get new coordinates
    coordinates = [x_slider.get(), y_slider.get(), z_slider.get()]

    # set new coordinates
    robot.ee = coordinates

    # use inverse kinematics to get new servo positions
    servo_3angles = np.round(np.rad2deg(robot.angles))

    # set the new positions to the servo sliders
    # negative servo2 and servo3 correcting for rotation orientation
    servo1_slider.set(servo_3angles[0])
    servo2_slider.set(-servo_3angles[1])
    servo3_slider.set(-servo_3angles[2])

#######################################
# directly set servo positions by inputting a number
#######################################
def servo1_set():
    # get new position
    new_servo1 = int(servo1_input.get())
    # set new position to slider
    servo1_slider.set(new_servo1)
def servo2_set():
    # get new position
    new_servo2 = int(servo2_input.get())
    # set new position to slider
    servo2_slider.set(new_servo2)
def servo3_set():
    # get new position
    new_servo3 = int(servo3_input.get())
    # set new position to slider
    servo3_slider.set(new_servo3)
def servo4_set():
    # get new position
    new_servo4 = int(servo4_input.get())
    # set new position to slider
    servo4_slider.set(new_servo4)
def servo5_set():
    # get new position
    new_servo5 = int(servo5_input.get())
    # set new position to slider
    servo5_slider.set(new_servo5)
def servo6_set():
    # get new position
    new_servo6 = int(servo6_input.get())
    # set new position to slider
    servo6_slider.set(new_servo6)

#######################################
# record/save positions
#######################################
# saving state, default True
# change this flag to False when stop recording
saving = True
# store saved positions in a list
saved_positions = []

# control save_state by a button
def save_state():
    global saving

    if saving == True:
        saving = False
        print(f'Save state: {saving}.')
    
    elif saving == False:
        saving = True
        print(f'Save state: {saving}.')

def save_positions():
    # `saving` is either True or False, controlled by the save_state button
    if saving:
        saved_positions.append([servo1_slider.get(), servo2_slider.get(), servo3_slider.get(), servo4_slider.get(), servo5_slider.get(), servo6_slider.get()]);
        print("last saved positions: "+str(saved_positions[-1]))
        
        # call itself again (recursive loop) after sleeping for `save_time`
        window.after(int(save_time*1000), save_positions)

#######################################
# play positions
#######################################
def play_positions():
    for position in saved_positions:
        # replay actions
        print("playing: "+str(position))
        send_positions(position)

        # sleep for `play_time` before playing the next action
        time.sleep(play_time)

    # update slider values to stop at the last played position, otherwise it will revert to the position before replaying
    servo1_slider.set(position[0])
    servo2_slider.set(position[1])
    servo3_slider.set(position[2])
    servo4_slider.set(position[3])
    servo5_slider.set(position[4])
    servo6_slider.set(position[5])

#######################################
# clear positions in `saved_positions`
#######################################
def clear_all_positions():
    global saved_positions
    saved_positions = []
    print("cleared all positions")

def clear_last_positions():
    global saved_positions
    removed = saved_positions.pop()
    print("removed: "+str(removed))
    print("saved positions: "+str(saved_positions))

#######################################
# open a txt file and load the positions to `saved_positions`
#######################################
def open_file():
    global saved_positions
    filename = filedialog.askopenfilename(initialdir = path, title = "Select a File", filetypes = (("Text files","*.txt*"),("all files","*.*")))
    file = open(filename, "r")
    data=file.read()
    saved_positions=eval(data)
    file.close()
    print("opened: "+filename)

#######################################
# save `saved_positions` to a txt file
#######################################
def save_file():
    save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    save_file.write(str(saved_positions))
    save_file.close()
    print("saved file")

#######################################
# instructions on how to use the GUI
#######################################
def instructions():
    print('''
    1. Setting the COM port of arduino:
    The active port (e.g. COM3) can be found in the Device Manager.

    2. Controlling the robot:
    You can control the robot by both forward and inverse kinematics.
    Forward kinematics: change the servo angles, update the x,y,z coordinates.
    Inverse kinematics: change the x,y,z coordinates, update the servo angles.

    The servo angles and x,y,z coordinates are continuously updated.
    You can change the slider values by dragging the sliders, or by using the specified keys on the keyboard.
    (see which keys control which sliders in the code)

    3. Saving actions:
    By clicking `Start saving`, you will start recording the servo angles every 0.1 seconds (the time interval can be changed).
    The servo angles will be saved to the list `saved_positions`.
    To stop the recording, `Change save state` to False.
    If you decide to save the recorded actions as a txt file, you can go to `File` -> `Save File`.

    To record the next series of actions, you need to first `Change save state` to True.
    Then simply `Start saving` again.
    Prior to the next save, you might also want to `Clear All Positions` to remove the actions in the temporary list of `saved_positions`.
    `Clear All Positions` will only clear the temporary list `saved_positions`, and will not affect your saved txt files.

    4. Replaying actions:
    `Replay Positions` will replay the positions in the `saved_positions` list.
    By default, `saved_positions` is an empty list.
    You will first have to record some actions in the list before replaying them.
    Alternatively, you can load the saved actions from a txt file to the `saved_positions` list, which can be done by going to `File` -> `Open File`.

    5. Resetting servos:
    `Reset servos` will reset the servos to the initial positions, which might be helpful before recording another set of actions.
    ''')

#%%
#######################################
# define tkinter GUI
#######################################
window = Tk()
window.title("Robot Arm Controller")
window.minsize(550,340)

# Button for setting the USB port
port_label=Label(window,text="Set Port:")
port_label.place(x=10,y=10)
port_input=Entry(window)
port_input.place(x=10,y=35)
port_button=Button(window, text="Enter", command=set_port)
port_button.place(x=135,y=32)

#%%
#######################################
# Sliders for servos (forward kinematics)
# the sliders can be controlled by dragging them or with keyboard keys
#######################################
# slider step controlled by keyboard keys
slider_step = 3

servo1_slider = Scale(window, from_=180, to=0, command = forward_kinematics)
servo1_slider.place(x=0, y=100)
servo1_slider.set(servo1)
window.bind("<a>", lambda e: servo1_slider.set(servo1_slider.get()+slider_step))
window.bind("<z>", lambda e: servo1_slider.set(servo1_slider.get()-slider_step))

servo1_label=Label(window,text="Servo 1")
servo1_label.place(x=10, y=80)

servo2_slider = Scale(window, from_=180, to=0, command = forward_kinematics)
servo2_slider.place(x=70, y=100)
servo2_slider.set(servo2)
window.bind("<s>", lambda e: servo2_slider.set(servo2_slider.get()+slider_step))
window.bind("<x>", lambda e: servo2_slider.set(servo2_slider.get()-slider_step))

servo2_label=Label(window,text="Servo 2")
servo2_label.place(x=80, y=80)

servo3_slider = Scale(window, from_=180, to=0, command = forward_kinematics)
servo3_slider.place(x=140, y=100)
servo3_slider.set(servo3)
window.bind("<d>", lambda e: servo3_slider.set(servo3_slider.get()+slider_step))
window.bind("<c>", lambda e: servo3_slider.set(servo3_slider.get()-slider_step))

servo3_label=Label(window,text="Servo 3")
servo3_label.place(x=150, y=80)

servo4_slider = Scale(window, from_=180, to=0)
servo4_slider.place(x=210, y=100)
servo4_slider.set(servo4)
window.bind("<f>", lambda e: servo4_slider.set(servo4_slider.get()+slider_step))
window.bind("<v>", lambda e: servo4_slider.set(servo4_slider.get()-slider_step))

servo4_label=Label(window,text="Servo 4")
servo4_label.place(x=220, y=80)

servo5_slider = Scale(window, from_=180, to=0)
servo5_slider.place(x=280, y=100)
servo5_slider.set(servo5)
window.bind("<g>", lambda e: servo5_slider.set(servo5_slider.get()+slider_step))
window.bind("<b>", lambda e: servo5_slider.set(servo5_slider.get()-slider_step))

servo5_label=Label(window,text="Servo 5")
servo5_label.place(x=290, y=80)

servo6_slider = Scale(window, from_=90, to=60)
servo6_slider.place(x=350, y=100)
servo6_slider.set(servo6)
window.bind("<h>", lambda e: servo6_slider.set(servo6_slider.get()+slider_step))
window.bind("<n>", lambda e: servo6_slider.set(servo6_slider.get()-slider_step))

servo6_label=Label(window,text="Servo 6")
servo6_label.place(x=360, y=80)

# apart from sliders, can also set values by inputting the degrees directly
servo1_input=Entry(window, width = 5)
servo1_input.place(x=15,y=210)
servo1_button=Button(window, text="Enter", command = servo1_set)
servo1_button.place(x=13,y=230)

servo2_input=Entry(window, width = 5)
servo2_input.place(x=85,y=210)
servo2_button=Button(window, text="Enter", command = servo2_set)
servo2_button.place(x=83,y=230)

servo3_input=Entry(window, width = 5)
servo3_input.place(x=155,y=210)
servo3_button=Button(window, text="Enter", command = servo3_set)
servo3_button.place(x=153,y=230)

servo4_input=Entry(window, width = 5)
servo4_input.place(x=225,y=210)
servo4_button=Button(window, text="Enter", command = servo4_set)
servo4_button.place(x=223,y=230)

servo5_input=Entry(window, width = 5)
servo5_input.place(x=295,y=210)
servo5_button=Button(window, text="Enter", command = servo5_set)
servo5_button.place(x=293,y=230)

servo6_input=Entry(window, width = 5)
servo6_input.place(x=365,y=210)
servo6_button=Button(window, text="Enter", command = servo6_set)
servo6_button.place(x=363,y=230)

#%%
#######################################
# Sliders for coordinates (inverse kinematics)
# the sliders can be controlled by dragging them or with keyboard keys
#######################################
# slider step controlled by keyboard keys
coordinate_step = 0.5

x_label=Label(window,text="x")
x_label.place(x=420, y=80)

x_slider = Scale(window, from_=-25, to=+25, resolution = 0.1, orient = 'horizontal', command = inverse_kinematics)
x_slider.place(x=430, y=60)
x_slider.set(coordinates[0])
window.bind("<Right>", lambda e: x_slider.set(x_slider.get()+coordinate_step))
window.bind("<Left>", lambda e: x_slider.set(x_slider.get()-coordinate_step))

y_label=Label(window,text="y")
y_label.place(x=420, y=130)

y_slider = Scale(window, from_=-25, to=+25, resolution = 0.1, orient = 'horizontal', command = inverse_kinematics)
y_slider.place(x=430, y=110)
y_slider.set(coordinates[1])
window.bind("<Up>", lambda e: y_slider.set(y_slider.get()+coordinate_step))
window.bind("<Down>", lambda e: y_slider.set(y_slider.get()-coordinate_step))

z_label=Label(window,text="z")
z_label.place(x=420, y=180)

z_slider = Scale(window, from_=-8, to=+31, resolution = 0.1, orient = 'horizontal', command = inverse_kinematics)
z_slider.place(x=430, y=160)
z_slider.set(coordinates[2])
window.bind("<'>", lambda e: z_slider.set(z_slider.get()+coordinate_step))
window.bind("</>", lambda e: z_slider.set(z_slider.get()-coordinate_step))

#%%
#######################################
# Buttons for recording and playing actions
#######################################
# Change save state
save_state_button=Button(window, text="Change save state", command=save_state)
save_state_button.place(x=10,y=260)

# Reset servos to default positions
servo_reset_button=Button(window, text="Reset servos", command=reset_servos)
servo_reset_button.place(x=10,y=295)

# Start saving/recording actions
save_button=Button(window, text="Start saving", command=save_positions)
save_button.place(x=120,y=260)

# Clear positions in `saved_positions`
clear_button=Button(window, text="Clear All Positions", command=clear_all_positions)
clear_button.place(x=120,y=295)

# Replay actions in `saved_positions`
play_button=Button(window, text="Replay Positions", command=play_positions)
play_button.place(x=250,y=260)

#%%
#######################################
# Menu bar
#######################################
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open File", command=open_file)
filemenu.add_command(label="Save File", command=save_file)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear last position", command=clear_last_positions)
editmenu.add_command(label="Clear all positions", command=clear_all_positions)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="How to use (printed in console)", command=instructions)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

#%%
#######################################
# while True loop
# 1. read the servo positions from the slider values
# 2. send the servo positions to arduino
#######################################
while True:
    window.update()
    if(port_opened):
        send_positions([servo1_slider.get(), servo2_slider.get(), servo3_slider.get(), servo4_slider.get(), servo5_slider.get(), servo6_slider.get()])
