import numpy as np


def pL(p):
    return 3*p*p - 2*p*p*p


def bare(p):
    return np.diag([1.0, 1.0-2.0*p, 1.0-2.0*p])


def qec(p):
    pl = pL(p)
    return np.diag([1.0, 1.0-2.0*pl, 1.0-2.0*pl])


for p in [0.01,0.05,0.1,0.2,0.3,0.4,0.49,0.5]:
    sb = np.linalg.svd(bare(p), compute_uv=False)
    sq = np.linalg.svd(qec(p), compute_uv=False)
    print(p, 'pL=', pL(p), 'bare=', sb, 'qec=', sq)
