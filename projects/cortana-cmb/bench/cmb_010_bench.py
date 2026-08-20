import numpy as np
from scipy.special import spherical_jn

chi_star = 14000.0
ells = np.arange(2,31)
nk = 120
k = np.logspace(-5,-2,nk)
dlnk = np.gradient(np.log(k))
Delta = np.array([0.2*spherical_jn(l,k*chi_star) for l in ells])
A = 4*np.pi*(Delta**2)*dlnk[None,:]

As, ns, kp = 2.1e-9, 0.965, 0.05
P = As*(k/kp)**(ns-1)
Cl = A @ P
sigma_cv = np.sqrt(2/(2*ells+1))*Cl
Aw = A/sigma_cv[:,None]

U,s,Vh = np.linalg.svd(Aw, full_matrices=True)
print("shape:", Aw.shape)
print("rank:", np.linalg.matrix_rank(Aw))
print("kernel dimension:", nk-np.linalg.matrix_rank(Aw))
print("condition number:", s[0]/s[-1])
print("relative singular values:", s/s[0])
