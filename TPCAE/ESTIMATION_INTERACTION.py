from compounds import SubstanceProp
from Models.MixtureModel import MixtureModel
import numpy as np
from scipy.optimize import brute


# def setK(model: MixtureModel, v: float):
#     n = model.getNumberOfSubstancesInSystem()
#     k = np.zeros((n, n), dtype=np.float64)
#     k[0][1] = v
#     k[1][0] = v
#     model.setBinaryInteractionsParameters(k)
#
#
# def getObjectiveFunction(model: MixtureModel, t, x_exp, y_exp, p_exp):
#
#     p_exp = np.atleast_1d(p_exp)
#
#     x1_exp = np.atleast_1d(x_exp)
#     x2_exp = 1.0 - x1_exp
#     lnx1 = np.log(x1_exp)
#     lnx2 = np.log(x2_exp)
#
#     y1_exp = np.atleast_1d(y_exp)
#     y2_exp = 1.0 - y1_exp
#     lny1 = np.log(y1_exp)
#     lny2 = np.log(y2_exp)
#
#     n_exp = len(x_exp)
#
#     lnphi1_liq = np.zeros(n_exp, dtype=np.float64)
#     lnphi2_liq = np.zeros(n_exp, dtype=np.float64)
#     lnphi1_vap = np.zeros(n_exp, dtype=np.float64)
#     lnphi2_vap = np.zeros(n_exp, dtype=np.float64)
#
#     for i in range(n_exp):
#         zs = model.system.getZfromPT(p_exp[i], t, [x1_exp[i], x2_exp[i]])
#         zl = np.min(zs)
#         lnphi1_liq[i] = np.log(
#             model.system.getPhi_i(0, [x1_exp[i], x2_exp[i]], p_exp[i], t, zl)
#         )
#         lnphi2_liq[i] = np.log(
#             model.system.getPhi_i(1, [x1_exp[i], x2_exp[i]], p_exp[i], t, zl)
#         )
#
#         zs = model.system.getZfromPT(p_exp[i], t, [y1_exp[i], y2_exp[i]])
#         zv = np.max(zs)
#         lnphi2_vap[i] = np.log(
#             model.system.getPhi_i(0, [y1_exp[i], y2_exp[i]], p_exp[i], t, zv)
#         )
#         lnphi2_vap[i] = np.log(
#             model.system.getPhi_i(1, [y1_exp[i], y2_exp[i]], p_exp[i], t, zv)
#         )
#
#     lnx1_plus_lnphi1_liq = lnx1 + lnphi1_liq
#     lnx2_plus_lnphi2_liq = lnx2 + lnphi2_liq
#     lny1_plus_lnphi1_vap = lny1 + lnphi1_vap
#     lny2_plus_lnphi2_vap = lny2 + lnphi2_vap
#
#     r1 = lnx1_plus_lnphi1_liq - lny1_plus_lnphi1_vap
#     r2 = lnx2_plus_lnphi2_liq - lny2_plus_lnphi2_vap
#
#     return np.sum(r2) + np.sum(r1)


ethane = SubstanceProp("ethane", "C2H6")
hydrogen_sulfide = SubstanceProp("hydrogen sulfide", "H2S")

eosname = "Peng and Robinson (1976)"
model = MixtureModel()
model.setEOS(eosname)
model.addSubstanceToSystem(ethane)
model.addSubstanceToSystem(hydrogen_sulfide)

x1_exp = [
    0.0241,
    0.0498,
    0.0849,
    0.1314,
    0.2264,
    0.3126,
    0.3938,
    0.5143,
    0.5847,
    0.6731,
    0.7639,
    0.8451,
    0.9026,
    0.951,
]


y1_exp = [
    0.1174,
    0.2013,
    0.2848,
    0.3716,
    0.4791,
    0.5334,
    0.5784,
    0.6388,
    0.6845,
    0.722,
    0.792,
    0.858,
    0.9031,
    0.9436,
]

p_exp = [
    1575452.66,
    1727137.38,
    1916743.28,
    2073254.332,
    2347665.78,
    2526929.54,
    2644140.46,
    2790309.372,
    2913036.1,
    2986810.032,
    3030247.02,
    3049552.348,
    3052310.252,
    3044726.016,
]
# algorithm


def setK(v: float):
    n = model.getNumberOfSubstancesInSystem()
    k = np.zeros((n, n), dtype=np.float64)
    k[0][1] = v
    k[1][0] = v
    model.setBinaryInteractionsParameters(k)


def getP_exp():
    return p_exp

def getx_exp():
    return x1_exp
def gety_exp():
    return y1_exp

t = 283.71
def getObjectiveFunction(k):
    setK(k)

    p_exp = getP_exp()
    x_exp = getx_exp()
    y_exp = gety_exp()

    p_exp = np.atleast_1d(p_exp)

    x1_exp = np.atleast_1d(x_exp)
    x2_exp = 1.0 - x1_exp

    y1_exp = np.atleast_1d(y_exp)
    y2_exp = 1.0 - y1_exp

    n_exp = len(x_exp)



    s = 0.0
    for i in range(n_exp):
        y, pb, pv,pl,k, it = model.system.getBubblePointPressure([x1_exp[i], x2_exp[i]],t)
        s += ((pb -p_exp[i] )/p_exp[i])**2
        x, pd, pv,pl,k, it = model.system.getDewPointPressure([y1_exp[i], y2_exp[i]],t)
        s += ((pd -p_exp[i] )/p_exp[i])**2


    return s


from time import time
s1 = time()
ans = brute(getObjectiveFunction, ((-.5,.5),), full_output=True)
s2 = time()
print(ans[0], ans[1])
print(s2 -s1)

# k0 = 0.07
# f0 = getObjectiveFunction( k0, t, x1_exp, y1_exp, p_exp)
#
# k1 = 0.08
# f1 = getObjectiveFunction( k1,t, x1_exp, y1_exp, p_exp)
#
# k2, f2 = 0, 0
#
# tol = 1e-10
# kmax = 10000
#
# k = 0
# for k in range(kmax):
#
#     k2 = k1 - f1 * (k1 - k0) / (f1 - f0)
#     f2 = getObjectiveFunction(k2, t, x1_exp, y1_exp, p_exp)
#
#     if np.abs(f2) < tol:
#         break
#
#     k0, f0 = k1, f1
#     k1, f1 = k2, f2
#
# print("iterations : ", k)
# print("f2: ", f2)
# print("K: ", k2)

