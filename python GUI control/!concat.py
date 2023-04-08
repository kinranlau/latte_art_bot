#%%
'''
This function concatenates a list of txt files, and outputs the concatenated actions as a txt file.
    Parameters:
            files (list): a list of txt files to be concatenated

    Returns:
            concat.txt: a txt file with the concatenated actions
'''

#%% 
files = ['1_first_turn_step10.txt',
'2_lift_jug_step2.txt',
'3_tilt_cup.txt',
'4_second_turn_easeinout20.txt',
'5_mix_in.txt',
'6_pre_shake_easeinout10.txt',
'7_shake_jug.txt',
'8_pre_rock_easeinout10.txt',
'9_rock_jug_execute.txt',
'10_reposition_jug_easeinout25.txt',
'11_tulip_1.txt',
'11.5_tulip_1to2_easeinout10.txt',
'12_tulip_2.txt',
'13_tulip_3.txt',
'14_replace_jug_easeinout10.txt']

all_positions = []
concat_filename = 'concat.txt'

# loop through the files and concat them to all_positions
for filename in files:
    file = open(filename, "r")
    data=file.read()
    saved_positions=eval(data)
    file.close()

    all_positions += saved_positions

# save the file
with open(concat_filename, 'w') as f:
    f.write(str(all_positions))
