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

file_list = open("input_displacement_to_LEI.txt", 'w')

for i, f in enumerate(data_file_list):
    if "orto_displacement" in f:
        file_list.write(data_dir + " " + f + "\n")