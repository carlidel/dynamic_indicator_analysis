import numpy as np
import subprocess
import h5py
import argparse
import os
import re

parser = argparse.ArgumentParser(
    description="Convert rev data to REI data",
    fromfile_prefix_chars='@'
)

parser.add_argument(
    "data_dir",
    help="data dir on eos"
)

parser.add_argument(
    "source_file",
    help="file to be used as input source"
)

parser.add_argument(
    "displacement_file",
    help="file with the displacement data"
)

args = parser.parse_args()
data_dir = args.data_dir
source_file = args.source_file
displacement_file = args.displacement_file

print("Gathering", displacement_file)
subprocess.run(["eos", "cp", os.path.join(data_dir, displacement_file), "."])

print("Gathering", source_file)
subprocess.run(["eos", "cp", os.path.join(data_dir, source_file), "."])

new_name = re.sub("inverse_tracking", "REI", displacement_file)

print("Executing script...")
subprocess.run([
    "python",
    "reversibility_to_REI.py",
    source_file,
    displacement_file,
    str(1),
    str(6),
    "-outname", new_name,
    "-outdir", ".",
])

print("Uploading back", new_name)
subprocess.run(["eos", "cp", new_name, data_dir])

print("Cleaning gathered files")
subprocess.run(["rm", displacement_file])
subprocess.run(["rm", source_file])
subprocess.run(["rm", new_name])
