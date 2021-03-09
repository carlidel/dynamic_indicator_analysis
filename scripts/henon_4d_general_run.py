import numpy as np
import subprocess
import os
import time
from tqdm import tqdm
import argparse

EXECUTING_LIST = {
    "long_tracking": False,
    "long_tracking_wk": False,
    "long_tracking_wk_bis": False,
    "long_tracking_wk_ter": False,
    "single_displacement": False,
    "orthonormal_displacement": False,
    "pure_inverse_tracking": False,
    "uniform_noisy_tracking": False,
    "gaussian_noisy_tracking": False,
    "uniform_noisy_tracking_fo": False,
    "gaussian_noisy_tracking_fo": False,
    "sali": False,
    "gali": True,
}

"""GALI AND FFT ARE INCLUDED BUT COMMENTED, BECAUSE THEY TAKE MUCH MUCH MORE TIME!!!"""

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
    "max_turns_long_run",
    help="turns to be done for the long tracking",
    type=int
)

parser.add_argument(
    "kick_magnitude",
    help="kick magnitude",
    type=float
)

parser.add_argument(
    "kick_sigma",
    help="kick sigma",
    type=float
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
    "tau",
    help="after how many steps you want SALI/GALI to be computed",
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
kick_magnitude = args.kick_magnitude
kick_sigma = args.kick_sigma

max_turns_long_run = args.max_turns_long_run

min_turns = args.min_turns
max_turns = args.max_turns
turn_samples = args.samples

tau = args.tau

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


if EXECUTING_LIST["long_tracking"]:
    start = time.time()
    print("Long Tracking")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track.py"),
        inputfile,
        str(max_turns_long_run),
        "-o",
        outdir
    ])

    end = time.time()
    print("Elapsed time:")
    print_elapsed_time(start, end)
    print("Total elapsed time so far:")
    print_elapsed_time(start_0, end)
    print("------------------")

if EXECUTING_LIST["long_tracking_wk"]:
    start = time.time()

    print("Long Tracking (with kicks)")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        inputfile,
        str(max_turns_long_run),
        str(1e-4),
        "1e-4",
        "-o",
        outdir
    ])

    end = time.time()
    print("Elapsed time:")
    print_elapsed_time(start, end)
    print("Total elapsed time so far:")
    print_elapsed_time(start_0, end)
    print("------------------")

if EXECUTING_LIST["long_tracking_wk_bis"]:
    start = time.time()

    print("Long Tracking (with kicks) bis")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        inputfile,
        str(max_turns_long_run),
        str(1e-8),
        "1e-8",
        "-o",
        outdir
    ])


    end = time.time()
    print("Elapsed time:")
    print_elapsed_time(start, end)
    print("Total elapsed time so far:")
    print_elapsed_time(start_0, end)
    print("------------------")

if EXECUTING_LIST["long_tracking_wk_ter"]:
    start = time.time()

    print("Long Tracking (with kicks) ter")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        inputfile,
        str(max_turns_long_run),
        str(1e-12),
        "1e-12",
        "-o",
        outdir
    ])

    end = time.time()
    print("Elapsed time:")
    print_elapsed_time(start, end)
    print("Total elapsed time so far:")
    print_elapsed_time(start_0, end)
    print("------------------")

if EXECUTING_LIST["single_displacement"]:
    start = time.time()

    print("Single displacement")

    id_secondary = "{:.0e}".format(displacement)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_track_displacement.py"),
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

if EXECUTING_LIST["orthonormal_displacement"]:
    start = time.time()

    print("Orthonormal displacement")

    id_secondary = "{:.0e}".format(displacement)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_track_orto_displacement.py"),
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

if EXECUTING_LIST["pure_inverse_tracking"]:
    start = time.time()

    print("Pure Inverse Tracking")

    id_secondary = "no_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "false",
        "false",
        str(displacement),
        str(0.0),
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

if EXECUTING_LIST["uniform_noisy_tracking"]:
    start = time.time()

    print("Uniform Noisy Tracking")

    id_secondary = "unif_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "true",
        str(kick_magnitude),
        str(0.0),
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

if EXECUTING_LIST["gaussian_noisy_tracking"]:
    start = time.time()

    print("Gaussian Noisy Tracking")

    id_secondary = "gauss_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "true",
        str(kick_magnitude),
        str(kick_sigma),
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

if EXECUTING_LIST["uniform_noisy_tracking_fo"]:
    start = time.time()

    print("Uniform Noisy Tracking (forward only)")

    id_secondary = "unif_kick_forward"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "false",
        str(kick_magnitude),
        str(0.0),
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

if EXECUTING_LIST["gaussian_noisy_tracking_fo"]:
    start = time.time()

    print("Gaussian Noisy Tracking (forward only)")

    id_secondary = "gauss_kick_forward"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "false",
        str(kick_magnitude),
        str(kick_sigma),
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

# start = time.time()
# print("Megno")
# id_secondary = "{:.0e}".format(displacement)
# subprocess.run([
#     "python",
#     os.path.join(scriptdir, "henon_4d_megno.py"),
#     inputfile,
#     str(min_turns),
#     str(max_turns),
#     str(turn_samples),
#     str(displacement),
#     id_secondary,
#     "-o",
#     outdir
# ])
# end = time.time()
# print("Elapsed time:")
# print_elapsed_time(start, end)
# print("Total elapsed time so far:")
# print_elapsed_time(start_0, end)
# print("------------------")

if EXECUTING_LIST["sali"]:
    start = time.time()

    print("Sali")

    id_secondary = "{:.0e}".format(displacement)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_sali.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement),
        str(tau),
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

if EXECUTING_LIST["gali"]:
    start = time.time()

    print("Gali")

    id_secondary = "{:.0e}".format(displacement)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_gali.py"),
        inputfile,
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement),
        str(tau),
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

# start = time.time()
# print("FFT computation")
# subprocess.run([
#     "python",
#     os.path.join(scriptdir, "henon_4d_fft_tracking.py"),
#     inputfile,
#     str(fft_min_power),
#     str(fft_max_power),
#     "-ncores",
#     str(2048),
#     "-o",
#     outdir
# ])
# end = time.time()
# print("Elapsed time:")
# print_elapsed_time(start, end)
# print("Total elapsed time so far:")
# print_elapsed_time(start_0, end)
# print("------------------")
