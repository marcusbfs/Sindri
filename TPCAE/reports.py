from utils import f2str
from units import pressure_options, temperature_options, volume_options, conv_unit
from IdealGasPropertiesPureSubstance import state_options


def format_reports(prop, **units):

    state = prop.state
    state_index = state_options.index(state)
    has_ig = True if prop.ideal is not None else False

    # units
    Tu = units["T"] if "T" in units else "K"
    Vu = units["V"] if "V" in units else "m3/mol"
    Pu = units["P"] if "P" in units else "Pa"
    rhou = units["rho"] if "rho" in units else "kg/m3"
    ene_per_molu = units["energy_per_mol"] if "energy_per_mol" in units else "J/mol"

    reportret = "fluid state: {0}\n".format(state)
    log = " --- LOG ---\n"

    def formatter(info, lval, vval):
        return "{0:<21}\t{1:>20}\t{2:>20}\n".format(info, lval, vval)

    reportret += formatter("Property", "Liquid", "Vapor")

    # Z, V and density
    Zl = f2str(prop.liq["Z"], 8, lt=1e-1)
    Zv = f2str(prop.vap["Z"], 8, lt=1e-1)

    Vs = "V [{0}]".format(Vu)
    Vl = f2str(conv_unit(prop.liq["V"], "m3/mol", Vu), 8, lt=1e-2, gt=1e4)
    Vv = f2str(conv_unit(prop.vap["V"], "m3/mol", Vu), 8, lt=1e-2, gt=1e4)

    rhos = "density [{0}]".format(rhou)
    rhol = f2str(conv_unit(prop.liq["rho"], "kg/m3", rhou), 8, lt=1e-2, gt=1e4)
    rhov = f2str(conv_unit(prop.vap["rho"], "kg/m3", rhou), 8, lt=1e-2, gt=1e4)

    reportret += formatter("Z", Zl, Zv)
    reportret += formatter(Vs, Vl, Vv)
    reportret += formatter(rhos, rhol, rhov)

    # Vapor pressure

    Pvps = "Pvp [{0}]".format(Pu)
    Pvpl = f2str(conv_unit(prop.Pvp, "Pa", Pu), 8, lt=1e-2, gt=1e4)
    Pvpv = f2str(conv_unit(prop.Pvp, "Pa", Pu), 8, lt=1e-2, gt=1e4)
    reportret += formatter(Pvps, Pvpl, Pvpv)

    # ideal property (if any)
    if has_ig:

        # Cp
        Cps = "Cp [{0}]".format("J mol-1 K-1")
        Cpl = f2str(prop.ideal["Cp"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(Cps, Cpl, Cpl)

        # Ideal properties
        dHIGs = "dH_IG [{0}]".format(ene_per_molu)
        dHIG = f2str(
            conv_unit(prop.ideal["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dHIGs, dHIG, dHIG)

        dSIGs = "dS_IG [{0}]".format("J mol-1 K-1")
        dSIG = f2str(prop.ideal["dS"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(dSIGs, dSIG, dSIG)

        dGIGs = "dG_IG [{0}]".format(ene_per_molu)
        dGIG = f2str(
            conv_unit(prop.ideal["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dGIGs, dGIG, dGIG)

        dUIGs = "dU_IG [{0}]".format(ene_per_molu)
        dUIG = f2str(
            conv_unit(prop.ideal["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dUIGs, dUIG, dUIG)

        dAIGs = "dA_IG [{0}]".format(ene_per_molu)
        dAIG = f2str(
            conv_unit(prop.ideal["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dAIGs, dAIG, dAIG)

        # real properties
        dHs = "dH [{0}]".format(ene_per_molu)
        dHliq = f2str(
            conv_unit(prop.liq["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dHvap = f2str(
            conv_unit(prop.vap["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dHs, dHliq, dHvap)

        dSs = "dS [{0}]".format("J mol-1 K-1")
        dSliq = f2str(prop.liq["dS"], 8, lt=1e-2, gt=1e4)
        dSvap = f2str(prop.vap["dS"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(dSs, dSliq, dSvap)

        dGs = "dG [{0}]".format(ene_per_molu)
        dGliq = f2str(
            conv_unit(prop.liq["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dGvap = f2str(
            conv_unit(prop.vap["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dGs, dGliq, dGvap)

        dUs = "dU [{0}]".format(ene_per_molu)
        dUliq = f2str(
            conv_unit(prop.liq["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dUvap = f2str(
            conv_unit(prop.vap["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dUs, dUliq, dUvap)

        dAs = "dA [{0}]".format(ene_per_molu)
        dAliq = f2str(
            conv_unit(prop.liq["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dAvap = f2str(
            conv_unit(prop.vap["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dAs, dAliq, dAvap)

    else:
        reportret += "Compound has no Cp equation parameters\n"

    # fugacity
    fs = "fugacity [{0}]".format(Pu)
    fliq = f2str(conv_unit(prop.liq["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
    fvap = f2str(conv_unit(prop.vap["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
    reportret += formatter(fs, fliq, fvap)

    return reportret
