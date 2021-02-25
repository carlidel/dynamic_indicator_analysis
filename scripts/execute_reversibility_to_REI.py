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
    if "inverse_tracking" in f:
        print("Gathering", f)
        subprocess.run(["eos", "cp", os.path.join(data_dir, f), "."])

        source_name = re.sub('orto_displacement', 'init', f)
        source_name = re.sub(r"_subid_.*\.", r"\.", source_name)
        print("Gathering", source_name)
        subprocess.run(["eos", "cp", os.path.join(data_dir, source_name), "."])

        new_name = re.sub("inverse_tracking", "REI", f)

        print("Executing script...")
        subprocess.run([
            "python",
            "reversibility_to_REI.py",
            source_name,
            f,
            str(1),
            str(6),
            "-outname", new_name,
            "-outdir", ".",
        ])

        print("Uploading back", new_name)
        subprocess.run(["eos", "cp", new_name, data_dir])

        print("Cleaning gathered files")
        subprocess.run(["rm", f])
        subprocess.run(["rm", source_name])
        subprocess.run(["rm", new_name])
