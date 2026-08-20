import numpy as np
from gardencore import analyze_operator, null_space, stack_channels, choose_next_measurement

def test_rank_kernel():
    A=np.array([[1,0,0],[0,1,0]],float)
    r=analyze_operator(A)
    assert r.rank==2 and r.kernel_dim==1

def test_null_space():
    A=np.array([[1,1]],float)
    N=null_space(A)
    assert N.shape==(2,1)
    assert np.linalg.norm(A@N) < 1e-12

def test_stack_channels():
    A=np.array([[1,0]],float)
    B=np.array([[0,1]],float)
    r=analyze_operator(stack_channels(A,B))
    assert r.rank==2 and r.kernel_dim==0

def test_choose_next_measurement():
    A=np.array([[1,0,0]],float)
    cands=[('redundant',np.array([2,0,0.])),('new',np.array([0,1,0.]))]
    best=choose_next_measurement(A,cands)
    assert best['label']=='new'
