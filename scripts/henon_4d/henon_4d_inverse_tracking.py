import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re
import sys

from uniform_sphere_sampling import sample_4d_sphere

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(
    description="Execute tracking and inverse tracking with and without kicks",
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
    "forward_kick",
    help="do you want kicks in the forward tracking?",
    type=str2bool
)

parser.add_argument(
    "backward_kick",
    help="do you want kicks in the backward tracking?",
    type=str2bool
)

parser.add_argument(
    "kick_module",
    help="module of the kicks",
    type=float
)

parser.add_argument(
    "kick_sigma",
    help="std of the kick module distribution (if 0, it's always the mean value)",
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

sub_id = args.sub_id

filename = "henon_4d_inverse_tracking_" + key + "_subid_" + sub_id + ".hdf5"

outdir = args.outdir
min_turns = args.min_turns
max_turns = args.max_turns
samples = args.samples
forward_kick = args.forward_kick
backward_kick = args.backward_kick
kick_module = args.kick_module
kick_sigma = args.kick_sigma

def compute_kicks(samples, module, sigma):
    x, px, y, py = sample_4d_sphere(samples)
    kicks = np.random.normal(module, sigma, samples)
    return x * kicks, px * kicks, y * kicks, py * kicks,

turn_list = np.logspace(
    np.log10(min_turns), np.log10(max_turns), samples, dtype=np.int)

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"]

x0 = source["coords/x"][...].flatten()
px0 = source["coords/px"][...].flatten()
y0 = source["coords/y"][...].flatten()
py0 = source["coords/py"][...].flatten()

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["min_turns"] = min_turns
dest.attrs["max_turns"] = max_turns
dest.attrs["samples"] = samples
dest.attrs["forward_kick"] = forward_kick
dest.attrs["backward_kick"] = backward_kick
dest.attrs["kick_module"] = kick_module
dest.attrs["kick_sigma"] = kick_sigma

for turns in turn_list:
    engine = hm.partial_track.generate_instance(x0, px0, y0, py0)
    print(turns)
    # Forward
    if not forward_kick:
        print("forward")
        engine.compute(turns, source.attrs["epsilon"], source.attrs["mu"])
    else:
        print("forward")
        engine.compute_with_kick(turns, source.attrs["epsilon"], source.attrs["mu"], kick_module=kick_module, kick_sigma=kick_sigma)

    # Backward
    if not backward_kick:
        print("backward")
        x, px, y, py, steps = engine.inverse_compute(
            turns, source.attrs["epsilon"], source.attrs["mu"])
    else:
        print("backward")
        x, px, y, py, steps = engine.inverse_compute_with_kick(
            turns, source.attrs["epsilon"], source.attrs["mu"], kick_module, kick_sigma)

    dest.create_dataset(
        "/{}/x".format(turns), data=x.reshape((side_cond, side_cond)))
    dest.create_dataset(
        "/{}/px".format(turns), data=px.reshape((side_cond, side_cond)))
    dest.create_dataset(
        "/{}/y".format(turns), data=y.reshape((side_cond, side_cond)))
    dest.create_dataset(
        "/{}/py".format(turns), data=py.reshape((side_cond, side_cond)))

source.close()
dest.close()
