import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re
from tqdm import tqdm

import uniform_sphere_sampling as uss


parser = argparse.ArgumentParser(
    description="Generates a MEGNO measurement.",
    fromfile_prefix_chars='@'
)

parser.add_argument(
    "input_file",
    help="file to be used as input source"
)

parser.add_argument(
    "min_turns",
    help="min amount of turns",
    type=int
)

parser.add_argument(
    "max_turns",
    help="max amount of turns",
    type=int
)

parser.add_argument(
    "samples",
    help="turn samples to be made in log spacing",
    type=int
)

parser.add_argument(
    "displacement",
    help="magnitude of the initial random displacement",
    type=float
)

parser.add_argument(
    "sub_id",
    help="sub id for this precise dataset",
    default="0"
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
filename = "henon_4d_megno_" + key + ".hdf5"

outdir = args.outdir
min_turns = args.min_turns
max_turns = args.max_turns
samples = args.samples
turn_list = np.logspace(
    np.log10(min_turns), np.log10(max_turns), samples, dtype=np.int)

displacement = args.displacement

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"] * 2

x0 = np.concatenate((source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten()))
px0 = np.concatenate((source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten()))
y0 = np.concatenate((source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten()))
py0 = np.concatenate((source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten()))

xk, pxk, yk, pyk = uss.sample_4d_sphere(source.attrs["total_samples"])

x0[total_cond//2:] += displacement * xk
px0[total_cond//2:] += displacement * pxk
y0[total_cond//2:] += displacement * yk
py0[total_cond//2:] += displacement * pyk

# Generate Data
engine = hm.partial_track.generate_instance(x0, px0, y0, py0)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["min_turns"] = min_turns
dest.attrs["max_turns"] = max_turns
dest.attrs["samples"] = samples
dest.attrs["displacement"] = displacement

dest.create_dataset(
    "/coords/x", data=x0[total_cond//2:].reshape((side_cond, side_cond)))
dest.create_dataset(
    "/coords/px", data=px0[total_cond//2:].reshape((side_cond, side_cond)))
dest.create_dataset(
    "/coords/y", data=y0[total_cond//2:].reshape((side_cond, side_cond)))
dest.create_dataset(
    "/coords/py", data=py0[total_cond//2:].reshape((side_cond, side_cond)))

epsilon = source.attrs["epsilon"]
mu = source.attrs["mu"]

sum = np.ones(source.attrs["total_samples"])
x1 = x0
px1 = px0
y1 = y0
py1 = py0

source.close()

for i in tqdm(range(0, max_turns)):
    x2, px2, y2, py2, _ = engine.compute(1, epsilon, mu)
    sum += (
        np.log(
            (
                + np.power(x2[:len(x2)//2] - x2[len(x2)//2:], 2)
                + np.power(px2[:len(x2)//2] - px2[len(x2)//2:], 2)
                + np.power(y2[:len(x2)//2] - y2[len(x2)//2:], 2)
                + np.power(py2[:len(x2)//2] - py2[len(x2)//2:], 2)
            ) / (
                + np.power(x1[:len(x1)//2] - x1[len(x1)//2:], 2)
                + np.power(px1[:len(x1)//2] - px1[len(x1)//2:], 2)
                + np.power(y1[:len(x1)//2] - y1[len(x1)//2:], 2)
                + np.power(py1[:len(x1)//2] - py1[len(x1)//2:], 2)
            )
        ) * (i + 1)
    )
    x1 = x2.copy()
    px1 = px2.copy()
    y1 = y2.copy()
    py1 = py2.copy()

    if i + 1 in turn_list:
        dest.create_dataset(
            "{}".format(i+1),
            data=sum.reshape((side_cond, side_cond))
        )

dest.close()