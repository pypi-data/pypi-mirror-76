import numpy as np
from numpy.linalg import multi_dot
from sklearn.preprocessing import normalize

__version__ = '0.1.0'


def SNF(Wall, K: int = 20, t: int = 20, alpha=1):
    """
    Python implementation of matlab version
    Parameters
    ----------
    Wall: all kernel matrices of size kxnxn
    K: number of neighbors, usually (10~30)
    t: number of iterations, usually (10~20)
    alpha: 1

    Returns
    -------

    """
    C, m, n = Wall.shape
    Wall = np.stack([normalize(Wi, norm='l1') for Wi in Wall])
    Wall = np.stack([(Wi + Wi.T) / 2 for Wi in Wall])

    W_dom = np.stack([_find_dominate_set(Wi, K) for Wi in Wall])

    W_sum = np.sum(Wall, axis=0)

    for _ in range(t):
        Wall0 = np.stack([multi_dot([W_dom[i], (W_sum - Wall[i]), W_dom[i].T]) / (C - 1) for i in range(C)])
        Wall = [_bo_normalized(W0i, alpha) for W0i in Wall0]
        W_sum = np.sum(Wall, axis=0)

    W = normalize(W_sum / C, norm='l1')
    return (W + W.T + np.eye(n)) / 2


def _bo_normalized(W, alpha=1):
    W = W + alpha * np.eye(W.shape[0])
    return (W + W.T) / 2


def _find_dominate_set(W, K):
    """
    Finds top K dominating columns on each row
    Parameters
    ----------
    W: matrix of mxn
    K: how many columns to keep

    Returns
    -------
    a matrix of mxn which have 0 for removed columns
    """
    # find cells to drop in each row
    to_drop = np.argsort(W, axis=1)[:, :-K]
    # remove cells except for top K in each row
    W_dom = W.copy()  # take copy to not mess original matrix
    for i in range(W.shape[0]):
        W_dom[i, to_drop[i]] = 0
    # normalize by new column sums
    return normalize(W_dom, norm='l1')
