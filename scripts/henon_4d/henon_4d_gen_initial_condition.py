import numpy as np
import henon_map as hm
import h5py
import argparse
import os
import sys

parser = argparse.ArgumentParser(
    description="Generates a dataset of initial conditions for a 4D modulated Hénon Map",
    fromfile_prefix_chars='@'
)

parser.add_argument(
    "id",
    help="id of the generated dataset"
)

parser.add_argument(
    "epsilon",
    help="epsilon value for modulation",
    type=float
)

parser.add_argument(
    "mu",
    help="mu value for modulation",
    type=float
)

parser.add_argument(
    "n_samples",
    help="n samples per side",
    type=int
)

parser.add_argument(
    "method",
    help="coordinate method for sampling the initial conditions",
    choices=["polar", "x_px", "y_py"],
    default="polar"
)

parser.add_argument(
    "extents",
    help="extents where you want to operate",
    nargs='*',
    default=[0,1,0,1,0,0]
)

parser.add_argument(
    "-outdir",
    action="store",
    help="output directory",
    default="./"
)

args = parser.parse_args()

id = args.id
outdir = args.outdir
epsilon = args.epsilon
mu = args.mu
n_samples = args.n_samples
extents = [float(a) for a in args.extents]
method = args.method

filename = "henon_4d_init_eps_{:.2}_mu_{:.2}_id_{}".format(
    epsilon, mu, id).replace(".", "_") + ".hdf5"

def compute_coords(extents, sampling, method="polar"):
    if method == "polar":
        x0 = np.linspace(extents[0], extents[1], sampling+2)[1:-1]
        y0 = np.linspace(extents[2], extents[3], sampling+2)[1:-1]
        xx, yy = np.meshgrid(x0, y0)
        xxf = xx * np.cos(extents[4])
        pxf = xx * np.sin(extents[4])
        yyf = yy * np.cos(extents[5])
        pyf = yy * np.sin(extents[5])
        return (xxf, pxf, yyf, pyf)
    elif method == "x_px":
        x0 = np.linspace(extents[0], extents[1], sampling+2)[1:-1]
        y0 = np.linspace(extents[2], extents[3], sampling+2)[1:-1]
        xx, yy = np.meshgrid(x0, y0)
        xxf = xx
        pxf = yy
        yyf = np.zeros_like(xxf)
        pyf = np.zeros_like(xxf)
        return (xxf, pxf, yyf, pyf)
    elif method == "y_py":
        x0 = np.linspace(extents[0], extents[1], sampling+2)[1:-1]
        y0 = np.linspace(extents[2], extents[3], sampling+2)[1:-1]
        xx, yy = np.meshgrid(x0, y0)
        yyf = xx
        pyf = yy
        xxf = np.zeros_like(yyf)
        pxf = np.zeros_like(yyf)
        return (xxf, pxf, yyf, pyf)

# Generate initial conditions

x, px, y, py = compute_coords(extents, n_samples, method)

dest = h5py.File(os.path.join(outdir, filename), mode="w")
dest.attrs["map_name"] = "Modulated Hénon map 4D"
dest.attrs["epsilon"] = epsilon
dest.attrs["mu"] = mu
dest.attrs["id"] = id
dest.attrs["samples"] = n_samples 
dest.attrs["total_samples"] = n_samples ** 2
dest.attrs["extents"] = extents
dest.attrs["sampling_method"] = method

dest.create_dataset("/coords/x", data=x)
dest.create_dataset("/coords/px", data=px)
dest.create_dataset("/coords/y", data=y)
dest.create_dataset("/coords/py", data=py)

dest.close()
