from sympy import *
from sympy import ImageSet, S

Z, deltal, Bl, thetal, epsilonl = symbols('Z deltal Bl thetal epsilonl', real=True)
a, b, P, R_IG, T, delta, theta, epsilon = symbols('a b P R_IG T delta theta epsilon', real=True)
alpha, omega = symbols('alpha omega', real=True)
Tc, Tr, Pc, Pr = symbols('Tc Tr Pc Pr', real=True)
V = symbols('V', real=True)

# pprint(eos_eq)


# eos_eq = Z ** 3 + (deltal - Bl - 1) * Z ** 2 + Z * (thetal + epsilonl - deltal * (Bl + 1)) - (
#         epsilonl * (Bl + 1) + Bl * thetal)
# eos_eq = eos_eq.subs(Bl, b*P/(R_IG*T))
# eos_eq = eos_eq.subs(deltal, delta*P/(R_IG*T))
# eos_eq = eos_eq.subs(thetal, theta*P/(R_IG*T)**2)
# eos_eq = eos_eq.subs(epsilonl, epsilon*(P/(R_IG*T))**2)
# print(eos_eq)
#
# # sZ = solve(eos_eq, Z)
# sZ=solveset(eos_eq, Z, S.Reals)
#
# # pprint(sZ)
#
# dZdT = diff(eos_eq, T)
# # print(dZdT)


Zf = V / (V - b) - ((theta / (R_IG * T) * V * (V - b))) / ((V - b) * (V ** 2 + delta * V + epsilon))
print(Zf)

eos = "van_der_waals_1890"
eos = "redlich_and_kwong_1949"
Pc_RTc = Pc / (R_IG * Tc)
Tr = T / Tc
Pr = P / Pc

if eos == "van_der_waals_1890":
    a = .42188 * (R_IG * Tc) ** 2 / Pc
    b = .125 / Pc_RTc
    delta = 0.
    epsilon = 0.
    alpha = 1.
    theta = a

elif eos == "redlich_and_kwong_1949":
    a = .42748 * (R_IG * Tc) ** 2 / Pc
    b = .08664 / Pc_RTc
    delta = 0.08664 / Pc_RTc
    epsilon = 0.
    alpha = 1. / Tr ** 0.5
    theta = a / Tr ** .5

Zf = V / (V - b) - ((theta / (R_IG * T) * V * (V - b))) / ((V - b) * (V ** 2 + delta * V + epsilon))
print(Zf)

Uf = T * diff(Zf, T) / V
print(Uf)
