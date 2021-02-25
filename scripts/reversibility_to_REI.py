import numpy as np
import h5py
import argparse
import os
import re


def make_REI_matrix(x0, px0, y0, py0, x, px, y, py):
    d_x = x - x0
    d_px = px - px0
    d_y = y - y0
    d_py = py - py0
    return np.transpose(np.array([
        [d_x * d_x, d_x * d_px, d_x * d_y, d_x * d_py],
        [d_px * d_x, d_px * d_px, d_px * d_y, d_px * d_py],
        [d_y * d_x, d_y * d_px, d_y * d_y, d_y * d_py],
        [d_py * d_x, d_py * d_px, d_py * d_y, d_py * d_py],
    ]), axes=(2, 3, 0, 1))


def faddeev_leverrier(m, grade=1):
    assert grade > 0
    step = 1
    B = m.copy()
    p = np.trace(B)
    while step != grade:
        step += 1
        B = np.matmul(m, B - np.identity(B.shape[-1]) * p)
        p = np.trace(B) * (1 / step)
    return p * ((-1) ** (grade + 1))


v_faddeev_leverrier = np.vectorize(
    faddeev_leverrier, signature="(n,m),(1)->(1)")


parser = argparse.ArgumentParser(
    description="Convert orto displacement data to LEI data",
    fromfile_prefix_chars='@'
)

parser.add_argument(
    "input_file",
    help="file to be used as input source"
)

parser.add_argument(
    "displacement_file",
    help="file with the displacement data"
)

parser.add_argument(
    "min_order",
    help="min order to consider",
    type=int
)

parser.add_argument(
    "max_order",
    help="max order to consider",
    type=int
)

parser.add_argument(
    "-outname",
    action="store",
    help="output name",
    default="LEI_data.hdf5"
)

parser.add_argument(
    "-outdir",
    action="store",
    help="output directory",
    default="./"
)

args = parser.parse_args()

input_file = args.input_file
displ_file = args.displacement_file
out_file = os.path.join(args.outdir, args.outname)

min_order = args.min_order
max_order = args.max_order

s = h5py.File(input_file, mode='r')
d = h5py.File(displ_file, mode='r')

out = h5py.File(out_file, mode='w')
out.attrs["inputfile"] = os.path.basename(input_file)

turns = list(d)
for t in turns:
    matrix = make_REI_matrix(
        s["coords/x"][...], s["coords/px"][...], s["coords/y"][...], s["coords/py"][...],
        d[t]["x"][...], d[t]["px"][...], d[t]["y"][...], d[t]["py"][...]
    )
    for i in range(min_order, max_order + 1):   
        data = v_faddeev_leverrier(matrix, [i])[:, :, 0]
        out.create_dataset(
            t + "/" + str(i),
            data=data
        )