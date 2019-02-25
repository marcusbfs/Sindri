from TPCAE.reports import *

from TPCAE.PureSubstance import PureSubstance

c = PureSubstance("Water", "H2O", "peng_and_robinson_1976")


propvl = c.all_calculations_at_P_T(0.0300720815 * 1e5, 300, 1e5, 273.16)

units = {
    "P": "bar",
    "T": "K",
    "V": "m3/mol",
    "rho": "kg/m3",
    "Cp": "J/K",
    "energy_per_mol": "J/mol",
}


def test_format_reports():
    retval = format_reports(propvl, **units)
    print(retval)
    # assert 0
