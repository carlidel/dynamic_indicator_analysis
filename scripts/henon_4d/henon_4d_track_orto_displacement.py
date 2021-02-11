import numpy as np
import henon_map as hm
import h5py
import ntpath
import argparse
import os
import re

parser = argparse.ArgumentParser(
    description="Generates an orthonormal displacement and executes a given set of trackings in log scale",
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

sub_id = args.sub_id

filename = "henon_4d_orto_displacement_" + key + "_subid_" + sub_id + ".hdf5"

outdir = args.outdir
min_turns = args.min_turns
max_turns = args.max_turns
samples = args.samples
displacement = args.displacement

turn_list = np.logspace(
    np.log10(min_turns), np.log10(max_turns), samples, dtype=np.int)
diff_list = turn_list[1:] - turn_list[:-1]

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"] * 5

x0 = np.concatenate((source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten(),
                     source["coords/x"][...].flatten()))
px0 = np.concatenate((source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten(),
                      source["coords/px"][...].flatten()))
y0 = np.concatenate((source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten(),
                     source["coords/y"][...].flatten()))
py0 = np.concatenate((source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten(),
                      source["coords/py"][...].flatten()))

x0[total_cond//5*1:total_cond//5*2] += displacement
px0[total_cond//5*2:total_cond//5*3] += displacement
y0[total_cond//5*3:total_cond//5*4] += displacement
py0[total_cond//5*4:] += displacement

engine = hm.partial_track.generate_instance(x0, px0, y0, py0)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]
dest.attrs["min_turns"] = min_turns
dest.attrs["max_turns"] = max_turns
dest.attrs["samples"] = samples
dest.attrs["displacement"] = displacement

x, px, y, py, steps = engine.compute(
    turn_list[0], source.attrs["epsilon"], source.attrs["mu"])

dest.create_dataset(
    "/{}/x".format(turn_list[0]),
    data=np.array([
        x[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
        x[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
        x[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
        x[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
        x[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
    ])
)
dest.create_dataset(
    "/{}/px".format(turn_list[0]),
    data=np.array([
        px[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
        px[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
        px[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
        px[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
        px[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
    ])
)
dest.create_dataset(
    "/{}/y".format(turn_list[0]),
    data=np.array([
        y[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
        y[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
        y[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
        y[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
        y[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
    ])
)
dest.create_dataset(
    "/{}/py".format(turn_list[0]),
    data=np.array([
        py[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
        py[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
        py[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
        py[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
        py[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
    ])
)

for i, turns in enumerate(diff_list):
    x, px, y, py, steps = engine.compute(
        turns, source.attrs["epsilon"], source.attrs["mu"])

    dest.create_dataset(
        "/{}/x".format(turn_list[i+1]),
        data=np.array([
            x[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
            x[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
            x[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
            x[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
            x[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
        ])
    )
    dest.create_dataset(
        "/{}/px".format(turn_list[i+1]),
        data=np.array([
            px[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
            px[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
            px[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
            px[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
            px[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
        ])
    )
    dest.create_dataset(
        "/{}/y".format(turn_list[i+1]),
        data=np.array([
            y[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
            y[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
            y[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
            y[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
            y[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
        ])
    )
    dest.create_dataset(
        "/{}/py".format(turn_list[i+1]),
        data=np.array([
            py[total_cond//5*0:total_cond//5*1].reshape((side_cond, side_cond)),
            py[total_cond//5*1:total_cond//5*2].reshape((side_cond, side_cond)),
            py[total_cond//5*2:total_cond//5*3].reshape((side_cond, side_cond)),
            py[total_cond//5*3:total_cond//5*4].reshape((side_cond, side_cond)),
            py[total_cond//5*4:total_cond//5*5].reshape((side_cond, side_cond)),
        ])
    )

source.close()
dest.close()
