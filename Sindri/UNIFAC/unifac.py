import numpy as np
import sqlite3

# db_file = "unifac_parameters.db"
db_file = "database.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

groups = ["CH3", "CH2", "CH2NH"]
vk = np.asarray([[2, 1, 1], [2, 5, 0]])
x = np.asarray([0.4, 0.6])
T = 308.15

# groups = ['CH3', 'CH2', 'OH', 'H2O']
# vk = np.asarray([[1,1,1,0], [0,0,0,1]])
# x = np.asarray([.5, 0])
# x[1] = 1. - x[0]
# T = 298.


n = len(vk)
m = len(groups)
k = np.zeros(m, dtype=np.int)
Rk = np.zeros(m, dtype=np.float64)
Qk = np.zeros(m, dtype=np.float64)
r = np.zeros(n, dtype=np.float64)
q = np.zeros(n, dtype=np.float64)
e = np.zeros((m, n), dtype=np.float64)
tau = np.zeros((m, m), dtype=np.float64)
beta = np.zeros((n, m), dtype=np.float64)
theta = np.zeros(m, dtype=np.float64)
s = np.zeros(m, dtype=np.float64)
amk = np.zeros((m, m), dtype=np.float64)
L = np.zeros(n, dtype=np.float64)
J = np.zeros(n, dtype=np.float64)
ln_gamma_C = np.zeros(n, dtype=np.float64)
ln_gamma_R = np.zeros(n, dtype=np.float64)

list_groups = ""
for i in range(m - 1):
    list_groups += "'" + groups[i] + "', "
list_groups += "'" + groups[-1] + "'"

for i in range(m):
    cursor.execute(
        "SELECT R,Q from subgroups where subgroup_name = '{}' order by number".format(
            groups[i]
        )
    )
    res = cursor.fetchone()
    Rk[i], Qk[i] = res
    query = "select number from maingroups where subgroups like '%[' || (select number from subgroups where subgroup_name = '{}')|| ']%'".format(
        groups[i]
    )
    cursor.execute(query)
    k[i] = cursor.fetchone()[0]

# amk
for _i in range(m):
    for _j in range(m):
        query = "select Aij, Aji from interaction_parameters where i = {} and j = {} order by i, j"
        cursor.execute(query.format(k[_i], k[_j]))
        res = cursor.fetchone()
        if res is not None:
            amk[_i][_j] = res[0]
            amk[_j][_i] = res[1]


conn.close()
# tau
tau = np.exp(-amk / T)

for i in range(n):
    r[i] = np.sum(vk[i] * Rk)
    q[i] = np.sum(vk[i] * Qk)

# r = np.sum(vk*Rk)

# r, q
for _k in range(m):
    for _i in range(n):
        e[_k][_i] = vk[_i][_k] * Qk[_k] / q[_i]


# beta
for _i in range(n):
    for _k in range(m):
        for _m in range(m):
            beta[_i][_k] += e[_m][_i] * tau[_m][_k]


for _k in range(m):
    sup_s = 0.0
    for _i in range(n):
        sup_s += x[_i] * q[_i] * e[_k][_i]
    theta[_k] = sup_s / np.sum(x * q)

for _k in range(m):
    for _m in range(m):
        s[_k] += theta[_m] * tau[_m][_k]

for _i in range(n):
    J[_i] = r[_i] / np.sum(r * x)
    L[_i] = q[_i] / np.sum(q * x)
    ln_gamma_C[_i] = (
        1.0
        - J[_i]
        + np.log(J[_i])
        - 5.0 * q[_i] * (1.0 - J[_i] / L[_i] + np.log(J[_i] / L[_i]))
    )

    _s = 0.0
    for _k in range(m):
        _s += theta[_k] * beta[_i][_k] / s[_k] - e[_k][_i] * np.log(
            beta[_i][_k] / s[_k]
        )
    ln_gamma_R[_i] = q[_i] * (1.0 - _s)

# print(amk)
gamma = np.exp(ln_gamma_C + ln_gamma_R)

print(gamma)
