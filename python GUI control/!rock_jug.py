#%%
'''
This function creates actions to rock (shake vertically) the jug.
This is achieved by rotating the wrist (servo 4) back and forth quickly.
    Parameters:
            filename (str): the txt file to read the last position
            shake_start (int): minimum angle of the wrist (servo 4) during the rocking action
            shake_end (int): maximum angle of the wrist (servo 4) during the rocking action
            shake_steps (int): number of steps getting from `shake_start` to `shake_end`, 1 is the fastest speed, >1 is slower
            shake_num (int): number of times to rock the jug

    Returns:
            filename_execute.txt: txt file containing the actions to rock the jug
'''
#%%
# txt file name to be read
filename = '9_rock_jug.txt'
# txt file name to be saved
save_name = filename.split('.txt')[0] + '_execute.txt'

# rocking action: rotate the wrist (servo 4) quickly to mix/shake the liquid in the milk jug
# start angle
shake_start = 145
# end angle
shake_end = 180
# rock speed, controlled by number of steps from shake_start to shake_end
shake_steps = 1
# shake step size
shake_step_size = int((shake_end - shake_start)/shake_steps)

# total number of times to shake
shake_num = 5

#%%
# open file
file = open(filename, "r")
data=file.read()
saved_positions=eval(data)

last_positions = saved_positions[-1]
file.close()

#%%
slight_shake = []

# first loop through total number of times to shake it
for i in range(shake_num):
    position = last_positions[:]
    # initialize servo 4 angle before shaking to `shake_end`
    position[3] = shake_end
    
    new_position = position[:]
    slight_shake.append(new_position)

    # decrease servo 4 angle by the `shake_step_size` until reaching the `shake_start` angle
    for step in range(shake_steps):
        position[3] -= shake_step_size

        new_position = position[:]
        slight_shake.append(new_position)

    # increase servo 4 angle by the `shake_step_size` until reaching the `shake_end` angle
    for step in range(shake_steps):
        position[3] += shake_step_size

        new_position = position[:]
        slight_shake.append(new_position)
#%%
# save to txt file
with open(save_name, 'w') as f:
    f.write(str(slight_shake))