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

for i, f in enumerate(data_file_list):
    if "orto_displacement" in f:
        print("Gathering", f)
        subprocess.run(["eos", "cp", os.path.join(data_dir, f), "."])
        
        new_name = re.sub("orto_displacement", "LEI", f)
        
        print("Executing script...")
        subprocess.run([
            "python",
            "displacement_to_LEI.py",
            os.path.join(data_dir, f),
            str(1),
            str(6),
            "-outname", new_name,
            "-outdir", ".",
        ])

        print("Uploading back", new_name)
        subprocess.run(["eos", "cp", new_name, data_dir])

        print("Cleaning gathered files")
        subprocess.run(["rm", f])
        subprocess.run(["rm", new_name])
