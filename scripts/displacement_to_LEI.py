import numpy as np
import h5py
import argparse
import os
import re


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

d = h5py.File(displ_file, mode='r')

out = h5py.File(out_file, mode='w')
out.attrs["inputfile"] = os.path.basename(input_file)

turns = list(d)
for t in turns:
    t11 = d[t]["x"][1] - d[t]["x"][0]
    t12 = d[t]["px"][1] - d[t]["px"][0]
    t13 = d[t]["y"][1] - d[t]["y"][0]
    t14 = d[t]["py"][1] - d[t]["py"][0]

    t21 = d[t]["x"][2] - d[t]["x"][0]
    t22 = d[t]["px"][2] - d[t]["px"][0]
    t23 = d[t]["y"][2] - d[t]["y"][0]
    t24 = d[t]["py"][2] - d[t]["py"][0]

    t31 = d[t]["x"][3] - d[t]["x"][0]
    t32 = d[t]["px"][3] - d[t]["px"][0]
    t33 = d[t]["y"][3] - d[t]["y"][0]
    t34 = d[t]["py"][3] - d[t]["py"][0]

    t41 = d[t]["x"][4] - d[t]["x"][0]
    t42 = d[t]["px"][4] - d[t]["px"][0]
    t43 = d[t]["y"][4] - d[t]["y"][0]
    t44 = d[t]["py"][4] - d[t]["py"][0]

    tm = np.transpose(np.array([
        [t11, t12, t13, t14],
        [t21, t22, t23, t24],
        [t31, t32, t33, t34],
        [t41, t42, t43, t44]
    ]), axes=(2, 3, 0, 1))
    tmt = np.transpose(tm, axes=(0, 1, 3, 2))
    tmttm = np.matmul(tmt, tm)

    for i in range(min_order, max_order + 1):
        data = v_faddeev_leverrier(tmttm, [i])[:, :, 0]
        out.create_dataset(
            t + "/" + str(i),
            data=data
        )