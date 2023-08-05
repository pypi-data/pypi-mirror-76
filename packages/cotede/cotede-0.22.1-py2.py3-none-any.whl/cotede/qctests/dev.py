

import numpy as np

def constant_cluster_size(x, tol=1e-4):
    """ Estimate the cluster size with constant value

        Returns how many consecutive neighbor values are equal or less than
          the given tolerance different.
    """
    dx = np.diff(x)
    fwd = np.zeros(np.shape(x), dtype='i')
    bwd = np.zeros(np.shape(x), dtype='i')
    idx = np.nonzero(np.absolute(dx) < tol)[0]

    for i in idx:
        fwd[i+1] = 1 + fwd[i]
    for i in idx[::-1]:
        bwd[i] = 1 + bwd[i+1]

    return fwd + bwd
