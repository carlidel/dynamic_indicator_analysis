import numpy as np
import subprocess
import os
import time
from tqdm import tqdm
import argparse


def print_elapsed_time(start, end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


parser = argparse.ArgumentParser(
    description="FFT 'smart' run",
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
    "fft_min_power",
    help="minimum 2** to consider",
    type=int
)

parser.add_argument(
    "fft_max_power",
    help="maximum 2** to consider",
    type=int
)

parser.add_argument(
    "sub_id",
    help="sub id for this precise dataset",
    default="0"
)

parser.add_argument(
    "extents",
    help="extents where you want to operate",
    nargs='*',
    default=[0, 1, 0, 1, 0, 0]
)

parser.add_argument(
    "-outdir",
    action="store",
    help="output directory",
    default="./"
)

args = parser.parse_args()

########## TODO::CHANGE WHEN NECESSARY ################
scriptdir = "./"
#######################################################
outdir = args.outdir

epsilon = args.epsilon
mu = args.mu

id_main = args.id
# Samples per side
side_samples = args.n_samples
# Sampling method
method = args.method
extents = args.extents

fft_min_power = args.fft_min_power
fft_max_power = args.fft_max_power

start_0 = time.time()
start_0 = time.time()

print("------------------")
print("Epsilon:", epsilon)
print("Mu:", mu)
print("------------------")

start = time.time()
print("Generate initial conditions")

subprocess.run([
    "python",
    os.path.join(scriptdir, "henon_4d_gen_initial_condition.py"),
    str(id_main),
    str(epsilon),
    str(mu),
    str(side_samples),
    str(method)] +
    [str(a) for a in extents] +
    ["-o", str(outdir)]
)

end = time.time()
print("Elapsed time:")
print_elapsed_time(start, end)
print("Total elapsed time so far:")
print_elapsed_time(start_0, end)
print("------------------")
start = time.time()

inputfile = os.path.join(
    outdir,
    "henon_4d_init_eps_{:.2}_mu_{:.2}_id_{}".format(
        epsilon, mu, id_main).replace(".", "_") + ".hdf5")

print("FFT computation")
subprocess.run([
    "python",
    os.path.join(scriptdir, "henon_4d_fft_tracking.py"),
    inputfile,
    str(fft_min_power),
    str(fft_max_power),
    "-ncores",
    str(512),
    "-o",
    outdir
])
end = time.time()
print("Elapsed time:")
print_elapsed_time(start, end)
print("Total elapsed time so far:")
print_elapsed_time(start_0, end)
print("------------------")
