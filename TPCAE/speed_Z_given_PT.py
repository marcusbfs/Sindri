import numpy as np
from time import time
from eos import EOS


c = EOS("Water", "H2O", "peng_and_robinson_1976")


n = 1000
Ptet = np.linspace(1e5, 10e5, n)
Ttet = np.linspace(280, 350, n)

times_per_exec = []

fvec = np.vectorize(c.return_Z_given_PT)

inic = time()
for p, t in zip(Ptet, Ttet):  # 17.96, .01796 per (n=1000)
    s1 = time()
    z = c.return_Z_numerically_given_PT(p, t)
    # z = c.return_Z_given_PT(p, t)
    s2 = time()
    times_per_exec.append(s2 - s1)


end = time()

print(
    "{0:.5f} seconds total ({1:.05f} sec per exec)".format(
        end - inic, np.average(np.asarray(times_per_exec))
    )
)
