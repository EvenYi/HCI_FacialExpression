#!/usr/bin/env python 

from subprocess import Popen, DEVNULL
import shlex, os, errno, time, glob

# Constants for later use
of2_verbose = False
temp_output = "of2_out"
temp_output_file = temp_output + '.csv'
landmark_count = 68

# This line finds the openface software
# If you're getting an error here, make sure this file is in the same folder as your openface installation
exe = ([exe for exe in glob.glob("./**/FeatureExtraction", recursive=True) if os.path.isfile(exe)] + [exe for exe in
                                                                                                      glob.glob(
                                                                                                          ".\\**\\FeatureExtraction.exe",
                                                                                                          recursive=True)])[
    0]

# Clean up the temp file from a previous run, if it exists
try:
    os.remove(temp_output_file)
except OSError as e:
    if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
        raise  # re-raise exception if a different error occurred

# These lines write the command to run openface with the correct options
command = shlex.split(" -device 0 -out_dir . -pose -2Dfp -of " + temp_output)
command.insert(0, exe)

# This line starts openface
of2 = Popen(command, stdin=DEVNULL, stdout=(None if of2_verbose else DEVNULL), stderr=DEVNULL)

# This loop waits until openface has actually started, as it can take some time to start producing output
while not os.path.exists(temp_output_file):
    time.sleep(.5)

# Openface saves info to a file, and we open that file here
data = open(temp_output_file, 'r')
# surprise = open('surprise.txt', 'w')


# This loop repeats while openface is still running
# Inside the loop, we read from the file that openface outputs to and check to see if there's anything new
# We handle the data if there is any, and wait otherwise
list_pitch = []
list_yaw = []
list_roll = []
brow_dist1_list = []
brow_dist2_list = []
eye_dist1_list = []
eye_dist2_list = []
mouth_long_list = []
mouth_width_list = []
pose_Tz_list = []
i = 0
while (of2.poll() == None):
    line = data.readline().strip()

    if (line != ""):
        try:
            # Parse the line and save the useful values
            of_values = [float(v) for v in line.split(', ')]
            # Yes No Indian Nod
            timestamp, confidence, success = of_values[2:5]
            pitch, yaw, roll = of_values[8:11]

            # no_data.write(str(yaw))
            # indian_nod.write(str(roll))
            #print(len(of_values))

            # Smile

            '''
            m_x_48 = of_values[269]
            m_x_54 = of_values[275]

            e_y_37 = of_values[258]
            e_y_41 = of_values[262]
            e_y_38 = of_values[259]
            e_y_40 = of_values[261]

            e_y_43 = of_values[264]
            e_y_47 = of_values[268]
            e_y_44 = of_values[265]
            e_y_46 = of_values[267]

            b_y_23 = of_values[244]
            b_y_20 = of_values[241]
            '''

            # surprise
            b_y_19 = of_values[98]
            e_y_38 = of_values[117]
            e_y_40 = of_values[119]

            b_y_24 = of_values[103]
            e_y_43 = of_values[122]
            e_y_47 = of_values[126]

            m_y_51 = of_values[130]
            m_y_57 = of_values[136]

            m_x_48 = of_values[59]
            m_x_54 = of_values[65]

            pose_Tz = of_values[7]

            landmarks = []
            for i in range(11, 11 + landmark_count):
                landmarks.append((of_values[i], of_values[i + landmark_count]))
        except ValueError:
            # This exception handles the header line
            continue

        # ********************************************
        # Most, maybe all, of your code will go here

        # if len(list_pitch) < 12:
        #     list_pitch.append(pitch)
        #     list_yaw.append(yaw)
        #     list_roll.append(roll)
        # else:
        #     # print(abs(b_y_19 - b_y_38))
        #     # print(abs(b_y_24 - b_y_43))
        #
        #     # print(m_y_51, m_y_57);
        #
        #     # print("pitch", max(list_pitch), min(list_pitch))
        #     #print("pitch", abs(max(list_pitch) - min(list_pitch)))
        #     #print("yaw", abs(max(list_yaw) - min(list_yaw)))
        #     #print("roll", abs(max(list_roll) - min(list_roll)))
        #
        #     if abs(max(list_pitch) - min(list_pitch)) >= 0.365 and abs(max(list_yaw) - min(list_yaw)) < 0.15 and abs(
        #             max(list_roll) - min(list_roll)) < 0.15:
        #         print("Yes")
        #     if abs(max(list_yaw) - min(list_yaw)) >= 0.3 and abs(max(list_pitch) - min(list_pitch)) < 0.15 and abs(
        #             max(list_roll) - min(list_roll)) < 0.15:
        #         print("No")
        #     if abs(max(list_roll) - min(list_roll)) >= 0.3 and abs(max(list_pitch) - min(list_pitch)) < 0.15 and abs(
        #         max(list_yaw) - min(list_yaw)) < 0.15:
        #         print("Indian Nod")

            # list_pitch = []
            # list_yaw = []
            # list_roll = []
        brow_dist1 = abs(b_y_19 - e_y_38)
        brow_dist2 = abs(b_y_24 - e_y_43)
        eye_dist1 = abs(e_y_38 - e_y_40)
        eye_dist2 = abs(e_y_43 - e_y_47)
        mouth_long = abs(m_y_51 - m_y_57)
        mouth_width = abs(m_x_48 - m_x_54)

        # surprise.write(str(brow_dist1) + '  ')
        # surprise.write(str(brow_dist2) + '  ')
        # surprise.write(str(eye_dist1) + '   ')
        # surprise.write(str(eye_dist2) + '   ')
        # surprise.write(str(mouth_long) + '  ')
        # surprise.write(str(mouth_width) + '\n')

        if len(brow_dist1_list) < 12:
            brow_dist1_list.append(brow_dist1)
            brow_dist2_list.append(brow_dist2)
            eye_dist1_list.append(eye_dist1)
            eye_dist2_list.append(eye_dist2)
            mouth_long_list.append(mouth_long)
            mouth_width_list.append(mouth_width)
            pose_Tz_list.append(pose_Tz)
        else:

            brow_abs1 = max(brow_dist1_list) - min(brow_dist1_list)
            brow_abs2 = max(brow_dist2_list) - min(brow_dist2_list)

            eye_abs1 = max(eye_dist1_list) - min(eye_dist1_list)
            eye_abs2 = max(eye_dist2_list) - min(eye_dist2_list)

            mouth_dist_abs = max(mouth_long_list) - min(mouth_long_list)
            pose_Tz_abs = max(pose_Tz_list) - min(pose_Tz_list)

            if brow_abs1 >= 3 and brow_abs2 >= 3 and eye_abs1 >= 0.3 and eye_abs2 >= 0.3 and 15 >= mouth_dist_abs >= 2 and pose_Tz_abs <= 30:
                print('SURPRISE!!!', i)
                i += 1

            brow_dist1_list = []
            brow_dist2_list = []
            eye_dist1_list = []
            eye_dist2_list = []
            mouth_long_list = []
            pose_Tz_list = []

    # ********************************************

    # Replace this line
    # print("time:", timestamp, "\tpitch:", pitch, "\tyaw:", yaw, "\troll:", roll)

    else:
        time.sleep(.01)

# Reminder: press 'q' to exit openface

print("Program ended")

data.close()
