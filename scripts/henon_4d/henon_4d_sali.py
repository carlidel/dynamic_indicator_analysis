from numba import njit
import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re
from tqdm import tqdm

import uniform_sphere_sampling as uss

@njit(parallel=True)
def sali(x, px, y, py):
    # build displacement vectors
    v1x = x[len(x)//3:(len(x)//3)*2] - x[:len(x)//3]
    v1px = px[len(x)//3:(len(x)//3)*2] - px[:len(x)//3]
    v1y = y[len(x)//3:(len(x)//3)*2] - y[:len(x)//3]
    v1py = py[len(x)//3:(len(x)//3)*2] - py[:len(x)//3]
    v2x = x[(len(x)//3)*2:] - x[:len(x)//3]
    v2px = px[(len(x)//3)*2:] - px[:len(x)//3]
    v2y = y[(len(x)//3)*2:] - y[:len(x)//3]
    v2py = py[(len(x)//3)*2:] - py[:len(x)//3]
    # compute norm
    norm1 = np.sqrt(np.power(v1x, 2) + np.power(v1px, 2) +
                    np.power(v1y, 2) + np.power(v1py, 2))
    norm2 = np.sqrt(np.power(v2x, 2) + np.power(v2px, 2) +
                    np.power(v2y, 2) + np.power(v2py, 2))
    # normalize
    v1x /= norm1
    v1px /= norm1
    v1y /= norm1
    v1py /= norm1
    v2x /= norm2
    v2px /= norm2
    v2y /= norm2
    v2py /= norm2
    # return minimum
    return np.sqrt(np.minimum(
        np.power(v1x + v2x, 2) + np.power(v1px + v2px, 2) +
        np.power(v1y + v2y, 2) + np.power(v1py + v2py, 2),
        np.power(v1x - v2x, 2) + np.power(v1px - v2px, 2) +
        np.power(v1y - v2y, 2) + np.power(v1py - v2py, 2)
    ))


parser = argparse.ArgumentParser(
    description="Generates a SALI measurement.",
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
    "tau",
    help="after how many steps you want SALI to be computed",
    type=int
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
filename = "henon_4d_sali_" + key + ".hdf5"

outdir = args.outdir
min_turns = args.min_turns
max_turns = args.max_turns
samples = args.samples
turn_list = np.logspace(
    np.log10(min_turns), np.log10(max_turns), samples, dtype=np.int)

displacement = args.displacement
tau = args.tau

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"] * 3

x0 = np.concatenate((source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten()))
px0 = np.concatenate((source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten()))
y0 = np.concatenate((source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten()))
py0 = np.concatenate((source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten()))

x0[total_cond//3*1:total_cond//3*2] += displacement
px0[total_cond//3*2:total_cond//3*3] += displacement

# Generate Data
engine = hm.partial_track.generate_instance(x0, px0, y0, py0)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["min_turns"] = min_turns
dest.attrs["max_turns"] = max_turns
dest.attrs["samples"] = samples
dest.attrs["displacement"] = displacement
dest.attrs["tau"] = tau


sali_value = sali(x0, px0, y0, py0)

counter = 0
for i in tqdm(range(0, (max_turns//tau)+5)):
    x, px, y, py, _ = engine.compute(
        tau, source.attrs["epsilon"], source.attrs["mu"])
    
    sali_value = np.amin([sali_value, sali(x,px,y,py)], axis=0)

    while i * tau > (turn_list[counter] if counter < len(turn_list) else np.inf):
        dest.create_dataset(
            "{}".format(turn_list[counter]),
            data=sali_value.reshape((side_cond, side_cond))
        )
        counter += 1

source.close()
dest.close()
