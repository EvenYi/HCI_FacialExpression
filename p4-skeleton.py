#!/usr/bin/env python 

from subprocess import Popen, DEVNULL
import shlex, os, errno, time, glob
import numpy as np

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
list_m_x_48_54 = []
list_m_y_51_57 = []
list_be_y_24_43 = []
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
            # print(len(of_values))

            # Smile

            m_y_51 = of_values[130]
            m_y_57 = of_values[136]
            m_x_48 = of_values[59]
            m_x_54 = of_values[65]
            e_y_37 = of_values[116]
            e_y_41 = of_values[120]
            e_y_38 = of_values[117]
            e_y_40 = of_values[119]
            e_y_43 = of_values[122]
            e_y_47 = of_values[126]
            e_y_44 = of_values[123]
            e_y_46 = of_values[125]
            b_y_24 = of_values[103]
            b_y_19 = of_values[98]

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

        if len(list_pitch) < 12:
            brow_dist1 = abs(b_y_19 - e_y_38)
            brow_dist2 = abs(b_y_24 - e_y_43)
            eye_dist1 = abs(e_y_38 - e_y_40)
            eye_dist2 = abs(e_y_43 - e_y_47)
            mouth_long = abs(m_y_51 - m_y_57)
            mouth_width = abs(m_x_48 - m_x_54)
            list_pitch.append(pitch)
            list_yaw.append(yaw)
            list_roll.append(roll)
            list_m_x_48_54.append(abs(m_x_48 - m_x_54))
            list_m_y_51_57.append(abs(m_y_51 - m_y_57))
            list_be_y_24_43.append(abs(b_y_24 - e_y_43))
            brow_dist1_list.append(brow_dist1)
            brow_dist2_list.append(brow_dist2)
            eye_dist1_list.append(eye_dist1)
            eye_dist2_list.append(eye_dist2)
            mouth_long_list.append(mouth_long)
            mouth_width_list.append(mouth_width)
            pose_Tz_list.append(pose_Tz)
        else:
            pose_Tz_avg = np.average(pose_Tz_list)

            rate = 500 / (pose_Tz_avg + 50)   # the rate for changing threshold based on distance between user and computer
            print(rate)

            brow_abs1 = max(brow_dist1_list) - min(brow_dist1_list)
            brow_abs2 = max(brow_dist2_list) - min(brow_dist2_list)

            eye_abs1 = max(eye_dist1_list) - min(eye_dist1_list)
            eye_abs2 = max(eye_dist2_list) - min(eye_dist2_list)

            mouth_dist_abs = max(mouth_long_list) - min(mouth_long_list)
            pose_Tz_abs = max(pose_Tz_list) - min(pose_Tz_list)

            if np.var(list_pitch) >= 0.005 * rate and abs(max(list_yaw) - min(list_yaw)) < 0.1 and abs(
                    max(list_roll) - min(list_roll)) < 0.1:
                print("Yes")
            elif abs(max(list_yaw) - min(list_yaw)) >= 0.2 and abs(max(list_pitch) - min(list_pitch)) < 0.1 and abs(
                    max(list_roll) - min(list_roll)) < 0.1:
                print("No")
            elif abs(max(list_roll) - min(list_roll)) >= 0.2 and abs(max(list_pitch) - min(list_pitch)) < 0.125 and abs(
                    max(list_yaw) - min(list_yaw)) < 0.125:
                print("Indian Nod")

            elif abs(max(list_yaw) - min(list_yaw)) < 0.1 and abs(max(list_pitch) - min(list_pitch)) < 0.1 and abs(
                    max(list_roll) - min(list_roll)) < 0.1 and abs(
                max(list_m_y_51_57) - min(list_m_y_51_57)) > 1 and abs(
                max(list_m_y_51_57) - min(list_m_y_51_57)) < 10 and abs(
                max(list_m_x_48_54) - min(list_m_x_48_54)) > 5.3 and abs(max(list_be_y_24_43) - min(list_be_y_24_43)) < 2.5:
                print("Smile")
            elif abs(max(list_yaw) - min(list_yaw)) < 0.15 and abs(max(list_pitch) - min(list_pitch)) < 0.15 and abs(
                    max(list_roll) - min(
                        list_roll)) < 0.15 and brow_abs1 >= 2.5 * rate and brow_abs2 >= 2.5 * rate \
                    and 15 * rate >= mouth_dist_abs >= 1.5 * rate:
                print('SURPRISE!!!')

            print('Pose_TZ', pose_Tz)
            print(brow_abs1, brow_abs2, mouth_dist_abs)
            list_pitch = []
            list_yaw = []
            list_roll = []
            brow_dist1_list = []
            brow_dist2_list = []
            eye_dist1_list = []
            eye_dist2_list = []
            mouth_long_list = []
            pose_Tz_list = []
            list_m_x_48_54 = []
            list_m_y_51_57 = []
            list_be_y_24_43 = []



# ********************************************

# Replace this line
# print("time:", timestamp, "\tpitch:", pitch, "\tyaw:", yaw, "\troll:", roll)

else:
    time.sleep(.01)

# Reminder: press 'q' to exit openface

print("Program ended")

data.close()
