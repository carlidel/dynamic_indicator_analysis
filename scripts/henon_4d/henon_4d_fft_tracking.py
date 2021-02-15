import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import re
from tqdm import tqdm
from numba import njit

@njit()
def interpolation(data, index):
    if np.any(np.isnan(data)):
        value = np.nan
    elif index == 0:
        value = 1
    else:
        if index == len(data) - 1:
            index -= 1
        cf1 = np.absolute(data[index - 1])
        cf2 = np.absolute(data[index])
        cf3 = np.absolute(data[index + 1])
        if cf3 > cf1:
            p1 = cf2
            p2 = cf3
            nn = index
        else:
            p1 = cf1
            p2 = cf2
            nn = index - 1            
        p3 = np.cos(2 * np.pi / len(data))
        value = (
            (nn / len(data)) + (1/np.pi) * np.arcsin(
                np.sin(2*np.pi/len(data)) * 
                ((-(p1+p2*p3)*(p1-p2) + p2*np.sqrt(p3**2*(p1+p2)**2 - 2*p1*p2*(2*p3**2-p3-1)))/(p1**2 + p2**2 + 2*p1*p2*p3))
            )
        )
    return np.absolute(1 - value)

parser = argparse.ArgumentParser(
    description="Track particles for a power of 2 turns and returns every interesting fft analysis!"
)

parser.add_argument(
    "input_file",
    help="file to be used as input source"
)

parser.add_argument(
    "min_power",
    help="min power turns to be considered for the fft",
    type=int
)

parser.add_argument(
    "max_power",
    help="power turns to be done for the fft",
    type=int
)

parser.add_argument(
    "-ncores",
    action="store",
    help="how many cpu cores to use for the computation",
    type=int,
    default=16
)

parser.add_argument(
    "-outdir",
    action="store",
    help="output directory",
    default="./"
)

args = parser.parse_args()

N_CORES = args.ncores

input_file = args.input_file
try:
    key = re.search(r'init_(.+?).hdf5', input_file).group(1)
except AttributeError:
    print("Something is wrong with the input filename!!")
    key = "weird"
filename = "henon_4d_fft_" + key + ".hdf5"
outdir = args.outdir
min_power = args.min_power
max_power = args.max_power

source = h5py.File(input_file, mode='r')

side_cond = source.attrs["samples"]
total_cond = source.attrs["total_samples"]

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["source_file"] = os.path.basename(input_file)
dest.attrs["id"] = source.attrs["id"]

max_turns = 2 ** max_power

dest.attrs["min_power"] = min_power
dest.attrs["power_turns"] = max_power

x0 = source["coords/x"][...].flatten()
px0 = source["coords/px"][...].flatten()
y0 = source["coords/y"][...].flatten()
py0 = source["coords/py"][...].flatten()

for i in tqdm(range(0, total_cond, N_CORES)):
    i_end = min(i + N_CORES, total_cond)

    engine = hm.partial_track.generate_instance(
        x0[i:i_end], px0[i:i_end], y0[i:i_end], py0[i:i_end],
        cuda_device=False
    )

    x, px, y, py = engine.compute(
        max_turns, source.attrs["epsilon"], source.attrs["mu"], full_track=True)
    
    for j in range(min_power, max_power + 1):
        steps = 2 ** (max_power - j)
        tune_x = dest.require_dataset(
            "/{}/tune_x".format(j),
            dtype=np.float64,
            shape=(steps, side_cond, side_cond))
        tune_y = dest.require_dataset(
            "/{}/tune_y".format(j),
            dtype=np.float64,
            shape=(steps, side_cond, side_cond))
        for k in range(steps):
            slice_l = k * (max_turns // steps)
            slice_r = (k + 1) * (max_turns // steps)

            signal = x[slice_l: slice_r] + 1j * px[slice_l: slice_r]
            fft_x = np.absolute(np.fft.fft(
                signal * np.hanning(signal.shape[0])[:,None], axis=0))

            signal = y[slice_l: slice_r] + 1j * py[slice_l: slice_r]
            fft_y = np.absolute(np.fft.fft(
                signal * np.hanning(signal.shape[0])[:,None], axis=0))
            
            for elem, true_i in enumerate(range(i,i_end)):
                value_x = np.argmax(fft_x[:, elem])
                value_x = interpolation(fft_x[:, elem], value_x)
                tune_x[k, true_i//side_cond, true_i % side_cond] = value_x
                value_y = np.argmax(fft_y[:, elem])
                value_y = interpolation(fft_y[:, elem], value_y)
                tune_y[k, true_i//side_cond, true_i % side_cond] = value_y

source.close()
dest.close()
