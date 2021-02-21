import numpy as np
import subprocess
import os
import itertools
from tqdm import tqdm

scriptdir = "henon_4d"
outdir = "../data"
inputdir = "../data"

epsilon_list = [0.0, 1.0, 16.0, 64.0]
mu_list = [0.0, -0.2, 0.2, -1.0, 1.0]
combos = list(itertools.product(mu_list, epsilon_list))

id_main = "basic_view"
# Samples per side
side_samples = 500
# Sampling method
method = "polar"
extents = [0.0, 1.0, 0.0, 1.0, 0.0, 0.0]

displacement_magnitude = 1e-12
displacement_sigma = 1e-13

max_turns_long_run = 10000000

min_turns = 10
max_turns = 100000
turn_samples = 51

tau = 100

fft_min_power = 8
fft_max_power = 14

to_do = {

}

for mu, epsilon in tqdm(combos[5:], desc="General computation"):
    print("------------------")
    print("Epsilon:", epsilon)
    print("Mu:", mu)
    print("------------------")
    print("Generate initial conditions")
    """
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
    """
    inputfile = "henon_4d_init_eps_{:.2}_mu_{:.2}_id_{}".format(
        epsilon, mu, id_main).replace(".", "_") + ".hdf5"

    print("Long Tracking")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track.py"),
        os.path.join(inputdir, inputfile),
        str(max_turns_long_run),
        "-o",
        outdir
    ])

    print("Long Tracking (with kicks)")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        os.path.join(inputdir, inputfile),
        str(max_turns_long_run),
        str(1e-6),
        "1e-6",
        "-o",
        outdir
    ])

    print("Long Tracking (with kicks) bis")
    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        os.path.join(inputdir, inputfile),
        str(max_turns_long_run),
        str(1e-8),
        "1e-8",
        "-o",
        outdir
    ])

    print("Long Tracking (with kicks) ter")

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_long_track_wkick.py"),
        os.path.join(inputdir, inputfile),
        str(max_turns_long_run),
        str(1e-12),
        "1e-12",
        "-o",
        outdir
    ])

    print("Single displacement")

    id_secondary = "{:.0e}".format(displacement_magnitude)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_track_displacement.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement_magnitude),
        id_secondary,
        "-o",
        outdir
    ])

    print("Orthonormal displacement")

    id_secondary = "{:.0e}".format(displacement_magnitude)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_track_orto_displacement.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement_magnitude),
        id_secondary,
        "-o",
        outdir
    ])

    print("Pure Inverse Tracking")

    id_secondary = "no_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "false",
        "false",
        str(displacement_magnitude),
        str(0.0),
        id_secondary,
        "-o",
        outdir
    ])

    print("Uniform Noisy Tracking")

    id_secondary = "unif_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "true",
        str(displacement_magnitude),
        str(0.0),
        id_secondary,
        "-o",
        outdir
    ])

    print("Gaussian Noisy Tracking")

    id_secondary = "gauss_kick"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "true",
        str(displacement_magnitude),
        str(displacement_sigma),
        id_secondary,
        "-o",
        outdir
    ])

    print("Uniform Noisy Tracking (forward only)")

    id_secondary = "unif_kick_forward"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "false",
        str(displacement_magnitude),
        str(0.0),
        id_secondary,
        "-o",
        outdir
    ])

    print("Gaussian Noisy Tracking (forward only)")

    id_secondary = "gauss_kick_forward"

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_inverse_tracking.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        "true",
        "false",
        str(displacement_magnitude),
        str(displacement_sigma),
        id_secondary,
        "-o",
        outdir
    ])

    print("Megno")

    id_secondary = "{:.0e}".format(displacement_magnitude)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_megno.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement_magnitude),
        id_secondary,
        "-o",
        outdir
    ])
