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

for mu, epsilon in tqdm(combos[:], desc="General computation"):
    print("------------------")
    print("Epsilon:", epsilon)
    print("Mu:", mu)
    print("------------------")
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

    inputfile = "henon_4d_init_eps_{:.2}_mu_{:.2}_id_{}".format(
        epsilon, mu, id_main).replace(".", "_") + ".hdf5"

    print("Sali")

    id_secondary = "{:.0e}".format(displacement_magnitude)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_sali.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement_magnitude),
        str(tau),
        id_secondary,
        "-o",
        outdir
    ])

    print("Gali")

    id_secondary = "{:.0e}".format(displacement_magnitude)

    subprocess.run([
        "python",
        os.path.join(scriptdir, "henon_4d_gali.py"),
        os.path.join(inputdir, inputfile),
        str(min_turns),
        str(max_turns),
        str(turn_samples),
        str(displacement_magnitude),
        str(tau),
        id_secondary,
        "-o",
        outdir
    ])
