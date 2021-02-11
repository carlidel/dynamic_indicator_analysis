import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re

parser = argparse.ArgumentParser(
    description="Track particles and saves every single step!"
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
filename = "henon_4d_verbose_track_" + key + ".hdf5"
outdir = args.outdir
max_turns = args.max_turns

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"]

engine = hm.partial_track.generate_instance(
    source["coords/x"][...].flatten(),
    source["coords/px"][...].flatten(),
    source["coords/y"][...].flatten(),
    source["coords/py"][...].flatten(),
)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["max_turns"] = max_turns

x_data = dest.create_dataset(
    "/coords/x", shape=(max_turns, side_cond, side_cond))
px_data = dest.create_dataset(
    "/coords/px", shape=(max_turns, side_cond, side_cond))
y_data = dest.create_dataset(
    "/coords/y", shape=(max_turns, side_cond, side_cond))
py_data = dest.create_dataset(
    "/coords/py", shape=(max_turns, side_cond, side_cond))

for i in range(max_turns):
    x, px, y, py, steps = engine.compute(
        1, source.attrs["epsilon"], source.attrs["mu"]
    )
    x_data[i] = x.reshape((side_cond, side_cond))
    px_data[i] = px.reshape((side_cond, side_cond))
    y_data[i] = y.reshape((side_cond, side_cond))
    py_data[i] = py.reshape((side_cond, side_cond))

source.close()
dest.close()
