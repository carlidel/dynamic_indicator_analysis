import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re

parser = argparse.ArgumentParser(
    description="Does a long run of a given initial condition file",
    fromfile_prefix_chars='@'
)

parser.add_argument(
    "input_file",
    help="file to be used as input source"
)

parser.add_argument(
    "max_turns",
    help="turns to be done for the tracking",
    type=int
)

parser.add_argument(
    "-outdir",
    action="store",
    help="output directory",
    default="./"
)

args = parser.parse_args()

input_file = args.input_file
try:
    key = re.search(r'init_(.+?).hdf5', input_file).group(1)
except AttributeError:
    print("Something is wrong with the input filename!!")
    key = "weird"
filename = "henon_4d_long_track_" + key + ".hdf5"
outdir = args.outdir
max_turns = args.max_turns

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"]

# Generate Data
engine = hm.partial_track.generate_instance(
    source["coords/x"][...].flatten(),
    source["coords/px"][...].flatten(),
    source["coords/y"][...].flatten(),
    source["coords/py"][...].flatten(),
)

x, px, y, py, steps = engine.compute(
    max_turns, source.attrs["epsilon"], source.attrs["mu"]
)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["max_turns"] = max_turns

dest.create_dataset("/coords/x", data=x.reshape((side_cond, side_cond)))
dest.create_dataset("/coords/px", data=px.reshape((side_cond, side_cond)))
dest.create_dataset("/coords/y", data=y.reshape((side_cond, side_cond)))
dest.create_dataset("/coords/py", data=py.reshape((side_cond, side_cond)))

dest.create_dataset(
    "stability_time", data=steps.reshape((side_cond, side_cond)))

source.close()
dest.close()
