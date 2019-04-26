import numpy as np

import db


def get_all_id_and_subgroups_formulas():
    query = """select number, subgroup_name
                 from unifac_subgroups 
                 order by number"""
    data = db.cursor.execute(query).fetchall()
    number_of_groups = len(data)
    ret_dict = {}
    for i in range(number_of_groups):
        value = int(data[i][0])
        key = "{:d} {}".format(value, data[i][1])
        ret_dict[key] = value

    return ret_dict


def has_unifac_in_db(subs_ids):
    cursor = db.cursor
    n = len(subs_ids)
    subs_ids = np.atleast_1d(subs_ids)
    for i in range(n):
        query = """select distinct us.subgroup_name
             from substance_unifac_subgroups sunifac inner join unifac_subgroups us on us.number = sunifac.subgroup_id
             where sunifac.substance_id ={} order by us.number""".format(
            subs_ids[0]
        )
        res = cursor.execute(query).fetchall()
        if len(res) < 1:
            return False
    return True


class UNIFAC:
    def __init__(self, subs_ids):

        cursor = db.cursor
        query = """select distinct us.subgroup_name
         from substance_unifac_subgroups sunifac inner join unifac_subgroups us on us.number = sunifac.subgroup_id
         where sunifac.substance_id in ({}) order by us.number""".format(
            ",".join("?" * len(subs_ids))
        )
        res = cursor.execute(query, subs_ids).fetchall()
        groups = []
        for g in res:
            groups.append(g[0])

        self.m = len(groups)
        self.n = len(subs_ids)
        self.vk = np.zeros((self.n, self.m), dtype=np.int64)
        for _i in range(self.n):
            for _j in range(self.m):
                query = """select frequency from substance_unifac_subgroups
                 where substance_id=? and subgroup_id=(select number from unifac_subgroups where subgroup_name=?)"""
                res = cursor.execute(query, (subs_ids[_i], groups[_j])).fetchone()
                if res is not None:
                    self.vk[_i][_j] = res[0]

        self.amk = np.zeros((self.m, self.m), dtype=np.float64)
        self.k = np.zeros(self.m, dtype=np.int64)
        self.Rk = np.zeros(self.m, dtype=np.float64)
        self.Qk = np.zeros(self.m, dtype=np.float64)

        list_groups = ""
        for i in range(self.m - 1):
            list_groups += "'" + groups[i] + "', "
        list_groups += "'" + groups[-1] + "'"

        for i in range(self.m):
            cursor.execute(
                "SELECT R,Q from unifac_subgroups where subgroup_name = '{}' order by number".format(
                    groups[i]
                )
            )
            res = cursor.fetchone()
            self.Rk[i], self.Qk[i] = res
            query = "select number from unifac_maingroups where subgroups like '%[' || (select number from unifac_subgroups where subgroup_name = '{}')|| ']%'".format(
                groups[i]
            )
            cursor.execute(query)
            self.k[i] = cursor.fetchone()[0]

        for _i in range(self.m):
            for _j in range(self.m):
                query = "select Aij, Aji from unifac_interaction_parameters where i = {} and j = {} order by i, j"
                cursor.execute(query.format(self.k[_i], self.k[_j]))
                res = cursor.fetchone()
                if res is not None:
                    self.amk[_i][_j] = res[0]
                    self.amk[_j][_i] = res[1]
        # cursor.close()

    def getGamma(self, x, T: float):
        x = np.atleast_1d(x)
        return _helper_getGamma(
            x, T, self.n, self.m, self.amk, self.vk, self.Rk, self.Qk
        )


from numba import njit, jit, float64, int8


@njit(
    "float64[:](float64[:], float64, int64, int64, float64[:,:], int64[:,:], float64[:], float64[:])",
    cache=True,
)
def _helper_getGamma(x, T: float, n, m, amk, vk, Rk, Qk):

    r = np.zeros(n, dtype=np.float64)
    q = np.zeros(n, dtype=np.float64)
    e = np.zeros((m, n), dtype=np.float64)
    beta = np.zeros((n, m), dtype=np.float64)
    theta = np.zeros(m, dtype=np.float64)
    s = np.zeros(m, dtype=np.float64)
    L = np.zeros(n, dtype=np.float64)
    J = np.zeros(n, dtype=np.float64)
    ln_gamma_C = np.zeros(n, dtype=np.float64)
    ln_gamma_R = np.zeros(n, dtype=np.float64)

    tau = np.exp(-amk / T)

    for i in range(n):
        r[i] = np.sum(vk[i] * Rk)
        q[i] = np.sum(vk[i] * Qk)

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

    gamma = np.exp(ln_gamma_C + ln_gamma_R)
    return gamma
