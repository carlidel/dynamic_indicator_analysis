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
    description="General run which generates most of the datasets",
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

displacement = args.displacement

min_turns = args.min_turns
max_turns = args.max_turns
turn_samples = args.samples

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

inputfile = os.path.join(
    outdir,
    "henon_4d_init_eps_{:.2}_mu_{:.2}_id_{}".format(
        epsilon, mu, id_main).replace(".", "_") + ".hdf5")

start = time.time()
print("Megno")
id_secondary = "{:.0e}".format(displacement)
subprocess.run([
    "python",
    os.path.join(scriptdir, "henon_4d_megno.py"),
    inputfile,
    str(min_turns),
    str(max_turns),
    str(turn_samples),
    str(displacement),
    id_secondary,
    "-o",
    outdir
])
end = time.time()
print("Elapsed time:")
print_elapsed_time(start, end)
print("Total elapsed time so far:")
print_elapsed_time(start_0, end)
print("------------------")
