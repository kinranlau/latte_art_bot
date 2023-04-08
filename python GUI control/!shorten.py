#%%
'''
This function shortens the list of actions by saving only every n actions.
    Parameters:
            filename (str): the txt file containing the list of actions
            read_step (int): reading step size, e.g. 5, only save one action every 5 actions

    Returns:
            filename_step{read_step}.txt: a txt file with the shortened actions
'''
#%%
# txt file name to be shortened
filename = '1_first_turn.txt'
# reading step size, e.g. 5, only save every 5 positions
read_step = 10

#%%
# open file
file = open(filename, "r")
data=file.read()
saved_positions=eval(data)
file.close()

# loop through the positions to shorten the list
short_saved_positions = []
for i in range(0, len(saved_positions), read_step):
    short_saved_positions.append(saved_positions[i])

# save the file
short_filename = filename.split('.txt')[0] + f'_step{read_step}.txt'
with open(short_filename, 'w') as f:
    f.write(str(short_saved_positions))
