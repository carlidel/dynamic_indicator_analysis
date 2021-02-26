import numpy as np
import subprocess
import h5py
import argparse
import os
import re

data_dir = "/eos/project/d/da-and-diffusion-studies/DA_Studies/Simulations/Models/dynamic_indicator_analysis/dynamic_indicator_analysis/data"

file_gathering = subprocess.run(
    ["eos", "ls", data_dir], stdout=subprocess.PIPE)

data_file_list = file_gathering.stdout.decode("utf-8").split("\n")[:-1]

file_list = open("input_reversibility_to_REI.txt", 'w')

for i, f in enumerate(data_file_list):
    if "inverse_tracking" in f:
        source_name = re.sub('orto_displacement', 'init', f)
        source_name = re.sub(r"_subid_.*\.", ".", source_name)
        file_list.write(data_dir + " " + source_name + " " + f + "\n")
