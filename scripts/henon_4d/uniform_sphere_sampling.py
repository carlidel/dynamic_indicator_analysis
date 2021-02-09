import numpy as np
from numba import njit, prange

@njit(parallel=True)
def extract_couples(samples):
    xi1 = np.empty(samples)
    xi2 = np.empty(samples)
    for i in prange(samples):
        a1 = np.random.uniform(-1, 1)
        a2 = np.random.uniform(-1, 1)
        while a1 ** 2 + a2 ** 2 >= 1:
            a1 = np.random.uniform(-1, 1)
            a2 = np.random.uniform(-1, 1)
        xi1[i] = a1
        xi2[i] = a2
    return xi1, xi2


def sample_4d_sphere(samples):
    """Samples points uniformely from a 4D sphere. The module is unitary.

    Parameters
    ----------
    samples : int
        number of samples desired

    Returns
    ----------
    tuple of arrays (x, px, y, py)
    """
    xi1, xi2 = extract_couples(samples)
    xi3, xi4 = extract_couples(samples)
    x = xi1
    px = xi2
    y = xi3 * np.sqrt(
        (1 - np.power(xi1, 2) - np.power(xi2, 2)) /
        (np.power(xi3, 2) + np.power(xi4, 2)))
    py = xi4 * np.sqrt(
        (1 - np.power(xi1, 2) - np.power(xi2, 2)) /
        (np.power(xi3, 2) + np.power(xi4, 2)))

    return x, px, y, py
