#%%
'''
This function interpolates the actions between the starting position and the final position.
It uses a sin ease-in-out function for the interpolation (see https://easings.net/).
    Parameters:
            filename (str): the txt file containing the starting (0) and final (-1) positions
            step_num (int): total number of steps including the starting, interpolated and final positions

    Returns:
            filename_easeinout{step_num}.txt: a txt file with the interpolated actions
'''
#%%
import numpy as np

# txt file to be read
# the first and last positions will be the starting and ending positions
filename = '13_replace_jug.txt'

# total number of steps for the whole motion/interpolation
step_num = 10

# txt file name to be saved
save_name = filename.split('.txt')[0] + f'_easeinout{step_num}.txt'

#%%
# define the ease-in-out function (sin ease-in-out)
def ease_in_out(array):
    output = 0.5 * (1 - np.cos(array * np.pi))
    return output

# map the x-values between 0 and 1 based on step_num
x_values = np.linspace(0, 1, step_num)
x_values = x_values.reshape(step_num, 1)

# get the corresponding ease-in-out values
ease_in_out_array = ease_in_out(x_values)

#%%
# read current servo positions from txt file
# open file
file = open(filename, "r")
data=file.read()
saved_positions=eval(data)

# get first and last positions
first_positions = np.array(saved_positions[0]).reshape(1, 6)
last_positions = np.array(saved_positions[-1]).reshape(1, 6)

# get the difference between first and last positions
diff = last_positions - first_positions

file.close()
#%%
# scale the ease-in-out output to the corresponding servos angles
# check: 
# ease_in_out_array.shape = (step_num, 1)
# diff.shape = (1, 6)
# first_positions.shape = (1, 6)
# scaled_ease_in_out.shape = (step_num, 6)
scaled_ease_in_out = np.matmul(ease_in_out_array, diff) + first_positions

# round to nearest integer
scaled_ease_in_out = scaled_ease_in_out.astype(int)

# read off the matrix, each row is one action
interpolated_positions = []
for row in scaled_ease_in_out:
    interpolated_positions.append(row.tolist())

#%%
# save to txt file
with open(save_name, 'w') as f:
    f.write(str(interpolated_positions))