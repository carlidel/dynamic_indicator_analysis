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
def compute_modules(x, px, y, py):
    v1x = x[len(x)//5:(len(x)//5)*2] - x[:len(x)//5]
    v1px = px[len(x)//5:(len(x)//5)*2] - px[:len(x)//5]
    v1y = y[len(x)//5:(len(x)//5)*2] - y[:len(x)//5]
    v1py = py[len(x)//5:(len(x)//5)*2] - py[:len(x)//5]
    v2x = x[(len(x)//5)*2:(len(x)//5)*3] - x[:len(x)//5]
    v2px = px[(len(x)//5)*2:(len(x)//5)*3] - px[:len(x)//5]
    v2y = y[(len(x)//5)*2:(len(x)//5)*3] - y[:len(x)//5]
    v2py = py[(len(x)//5)*2:(len(x)//5)*3] - py[:len(x)//5]
    v3x = x[(len(x)//5)*3:(len(x)//5)*4] - x[:len(x)//5]
    v3px = px[(len(x)//5)*3:(len(x)//5)*4] - px[:len(x)//5]
    v3y = y[(len(x)//5)*3:(len(x)//5)*4] - y[:len(x)//5]
    v3py = py[(len(x)//5)*3:(len(x)//5)*4] - py[:len(x)//5]
    v4x = x[(len(x)//5)*4:] - x[:len(x)//5]
    v4px = px[(len(x)//5)*4:] - px[:len(x)//5]
    v4y = y[(len(x)//5)*4:] - y[:len(x)//5]
    v4py = py[(len(x)//5)*4:] - py[:len(x)//5]
    # compute norm
    norm1 = np.sqrt(np.power(v1x, 2) + np.power(v1px, 2) +
                    np.power(v1y, 2) + np.power(v1py, 2))
    norm2 = np.sqrt(np.power(v2x, 2) + np.power(v2px, 2) +
                    np.power(v2y, 2) + np.power(v2py, 2))
    norm3 = np.sqrt(np.power(v3x, 2) + np.power(v3px, 2) +
                    np.power(v3y, 2) + np.power(v3py, 2))
    norm4 = np.sqrt(np.power(v4x, 2) + np.power(v4px, 2) +
                    np.power(v4y, 2) + np.power(v4py, 2))
    # normalize
    v1x /= norm1
    v1px /= norm1
    v1y /= norm1
    v1py /= norm1
    v2x /= norm2
    v2px /= norm2
    v2y /= norm2
    v2py /= norm2
    v3x /= norm3
    v3px /= norm3
    v3y /= norm3
    v3py /= norm3
    v4x /= norm4
    v4px /= norm4
    v4y /= norm4
    v4py /= norm4

    return v1x, v1px, v1y, v1py, v2x, v2px, v2y, v2py, v3x, v3px, v3y, v3py, v4x, v4px, v4y, v4py


def gali(matrix4, matrix3, matrix2, n_samples):    
    # SVD4
    bool_mask = np.all(np.logical_not(np.isnan(matrix4)), axis=(1, 2))
    _, s, _ = np.linalg.svd(matrix4[bool_mask], full_matrices=True)
    result4 = np.zeros((n_samples))
    result4[np.logical_not(bool_mask)] = np.nan
    result4[bool_mask] = np.prod(s, axis=-1)
    
    # SVD3
    bool_mask = np.all(np.logical_not(np.isnan(matrix3)), axis=(1, 2))
    _, s, _ = np.linalg.svd(matrix3[bool_mask], full_matrices=True)
    result3 = np.zeros((n_samples))
    result3[np.logical_not(bool_mask)] = np.nan
    result3[bool_mask] = np.prod(s, axis=-1)

    # SVD2
    bool_mask = np.all(np.logical_not(np.isnan(matrix2)), axis=(1, 2))
    _, s, _ = np.linalg.svd(matrix2[bool_mask], full_matrices=True)
    result2 = np.zeros((n_samples))
    result2[np.logical_not(bool_mask)] = np.nan
    result2[bool_mask] = np.prod(s, axis=-1)

    return result4, result3, result2

parser = argparse.ArgumentParser(
    description="Generates a GALI measurement.",
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
    help="after how many steps you want GALI to be computed",
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
filename = "henon_4d_gali_" + key + ".hdf5"

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
py0[total_cond//5*4:total_cond//5*5] += displacement

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

v1x, v1px, v1y, v1py, v2x, v2px, v2y, v2py, v3x, v3px, v3y, v3py, v4x, v4px, v4y, v4py = compute_modules(x0, px0, y0, py0)
matrix4 = np.array(
    [[v1x, v2x, v3x, v4x],
     [v1px, v2px, v3px, v4px],
     [v1y, v2y, v3y, v4y],
     [v1py, v2py, v3py, v4py]]
)
matrix3 = np.array(
    [[v1x, v2x, v3x],
     [v1px, v2px, v3px],
     [v1y, v2y, v3y],
     [v1py, v2py, v3py]]
)
matrix2 = np.array(
    [[v1x, v2x],
     [v1px, v2px],
     [v1y, v2y],
     [v1py, v2py]]
)
matrix4 = np.swapaxes(matrix4, 1, 2)
matrix4 = np.swapaxes(matrix4, 0, 1)

matrix3 = np.swapaxes(matrix3, 1, 2)
matrix3 = np.swapaxes(matrix3, 0, 1)

matrix2 = np.swapaxes(matrix2, 1, 2)
matrix2 = np.swapaxes(matrix2, 0, 1)
gali4, gali3, gali2 = gali(matrix4, matrix3, matrix2,
                           source.attrs["total_samples"])

counter = 0
for i in tqdm(range(0, (max_turns//tau)+1)):
    x, px, y, py, _ = engine.compute(
        tau, source.attrs["epsilon"], source.attrs["mu"])

    v1x, v1px, v1y, v1py, v2x, v2px, v2y, v2py, v3x, v3px, v3y, v3py, v4x, v4px, v4y, v4py = compute_modules(x, px, y, py)
    matrix4 = np.array(
        [[v1x, v2x, v3x, v4x],
         [v1px, v2px, v3px, v4px],
         [v1y, v2y, v3y, v4y],
         [v1py, v2py, v3py, v4py]]
    )
    matrix3 = np.array(
        [[v1x, v2x, v3x],
         [v1px, v2px, v3px],
         [v1y, v2y, v3y],
         [v1py, v2py, v3py]]
    )
    matrix2 = np.array(
        [[v1x, v2x],
         [v1px, v2px],
         [v1y, v2y],
         [v1py, v2py]]
    )
    matrix4 = np.swapaxes(matrix4, 1, 2)
    matrix4 = np.swapaxes(matrix4, 0, 1)

    matrix3 = np.swapaxes(matrix3, 1, 2)
    matrix3 = np.swapaxes(matrix3, 0, 1)

    matrix2 = np.swapaxes(matrix2, 1, 2)
    matrix2 = np.swapaxes(matrix2, 0, 1)
    gali4_n, gali3_n, gali2_n = gali(
        matrix4, matrix3, matrix2, source.attrs["total_samples"])
    
    gali4 = np.amin([gali4, gali4_n], axis=0)
    gali3 = np.amin([gali3, gali2_n], axis=0)
    gali2 = np.amin([gali3, gali2_n], axis=0)

    while i * tau > turn_list[counter]:
        dest.create_dataset(
            "gali4/{}".format(turn_list[counter]),
            data=gali4.reshape((side_cond, side_cond))
        )
        dest.create_dataset(
            "gali3/{}".format(turn_list[counter]),
            data=gali4.reshape((side_cond, side_cond))
        )
        dest.create_dataset(
            "gali2/{}".format(turn_list[counter]),
            data=gali4.reshape((side_cond, side_cond))
        )
        counter += 1

source.close()
dest.close()
