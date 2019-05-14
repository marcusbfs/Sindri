from Properties import VaporPressure, Props
from units import conv_unit
from utils import f2str


def tablewidget_vap_liq_reports(pliq: Props, pvap: Props, pvp: VaporPressure, **units):
    """
    Generates a table-formatted calculations report.

    Parameters
    ----------
    pliq : Props
        liquid properties to be reported
    pvap : Props
        vapor properties to be reported
    pvp : VaporPressure
        vapor pressure(s) to be reported
    units : kwarg
        units in which the results will be reported

    Returns
    -------
    labels : list of str
        formatted properties labels
    liq_values : list of str
        formatted liquid properties
    vap_values : list of str
        formatted vapor properties

    """

    labels = []
    liq_values = []
    vap_values = []

    has_ig = True if pliq.IGProps != 0 else False

    # units
    Tu = units["T"] if "T" in units else "K"
    Vu = units["V"] if "V" in units else "m3/mol"
    Pu = units["P"] if "P" in units else "Pa"
    rhou = units["rho"] if "rho" in units else "kg/m3"
    ene_per_molu = units["energy_per_mol"] if "energy_per_mol" in units else "J/mol"
    ene_per_mol_tempu = (
        units["energy_per_mol_temp"] if "energy_per_mol_temp" in units else "J/molK"
    )
    # Z, V and density
    Zl = f2str(pliq.Z, 6, lt=1e-1)
    Zv = f2str(pvap.Z, 6, lt=1e-1)
    labels.append("Z")
    liq_values.append(Zl)
    vap_values.append(Zv)

    Vs = "V [{0}]".format(Vu)
    Vl = f2str(conv_unit(pliq.V, "m3/mol", Vu), 6, lt=1e-2, gt=1e4)
    Vv = f2str(conv_unit(pvap.V, "m3/mol", Vu), 6, lt=1e-2, gt=1e4)
    labels.append(Vs)
    liq_values.append(Vl)
    vap_values.append(Vv)

    if pliq.rho and pvap.rho:
        rhos = "Density [{0}]".format(rhou)
        rhol = f2str(conv_unit(pliq.rho, "kg/m3", rhou), 6, lt=1e-2, gt=1e4)
        rhov = f2str(conv_unit(pvap.rho, "kg/m3", rhou), 6, lt=1e-2, gt=1e4)
        labels.append(rhos)
        liq_values.append(rhol)
        vap_values.append(rhov)

    # Vapor pressure

    if pvp.EOS:
        Pvpeoss = "Vap. P (EOS) [{0}]".format(Pu)
        Pvpeosl = f2str(conv_unit(pvp.EOS, "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(Pvpeoss)
        liq_values.append(Pvpeosl)
        vap_values.append(Pvpeosl)

    if pvp.AW:
        PvpAWs = "Vap. P (Ambrose-Walton) [{0}]".format(Pu)
        PvpAWl = f2str(conv_unit(pvp.AW, "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(PvpAWs)
        liq_values.append(PvpAWl)
        vap_values.append(PvpAWl)

        PvpLKs = "Vap. P (Lee-Kesler) [{0}]".format(Pu)
        PvpLKl = f2str(conv_unit(pvp.LK, "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(PvpLKs)
        liq_values.append(PvpLKl)
        vap_values.append(PvpLKl)

        #
    if pvp.Antoine:
        PvpAntoines = "Vap. P (Antoine) [{0}]".format(Pu)
        PvpAntoinel = f2str(conv_unit(pvp.Antoine, "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(PvpAntoines)
        liq_values.append(PvpAntoinel)
        vap_values.append(PvpAntoinel)

    # real properties (if any)
    if has_ig:

        # real properties
        dHs = "H [{0}]".format(ene_per_molu)
        dHliq = f2str(
            conv_unit(pliq.Props.H, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dHvap = f2str(
            conv_unit(pvap.Props.H, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dHs)
        liq_values.append(dHliq)
        vap_values.append(dHvap)

        dSs = "S [{0}]".format(ene_per_mol_tempu)
        dSliq = f2str(
            conv_unit(pliq.Props.S, "J/molK", ene_per_mol_tempu), 6, lt=1e-2, gt=1e4
        )
        dSvap = f2str(
            conv_unit(pvap.Props.S, "J/molK", ene_per_mol_tempu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dSs)
        liq_values.append(dSliq)
        vap_values.append(dSvap)

        dGs = "G [{0}]".format(ene_per_molu)
        dGliq = f2str(
            conv_unit(pliq.Props.G, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dGvap = f2str(
            conv_unit(pvap.Props.G, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dGs)
        liq_values.append(dGliq)
        vap_values.append(dGvap)

        dUs = "U [{0}]".format(ene_per_molu)
        dUliq = f2str(
            conv_unit(pliq.Props.U, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dUvap = f2str(
            conv_unit(pvap.Props.U, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dUs)
        liq_values.append(dUliq)
        vap_values.append(dUvap)

        dAs = "A [{0}]".format(ene_per_molu)
        dAliq = f2str(
            conv_unit(pliq.Props.A, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dAvap = f2str(
            conv_unit(pvap.Props.A, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dAs)
        liq_values.append(dAliq)
        vap_values.append(dAvap)

        # fugacity
        fs = "Fugacity [{0}]".format(Pu)
        fliq = f2str(conv_unit(pliq.Fugacity, "Pa", Pu), 8, lt=1e-2, gt=1e4)
        fvap = f2str(conv_unit(pvap.Fugacity, "Pa", Pu), 8, lt=1e-2, gt=1e4)
        labels.append(fs)
        liq_values.append(fliq)
        vap_values.append(fvap)

        # Ideal properties
        # Cp
        Cps = "Cp [{0}]".format(ene_per_mol_tempu)
        Cpl = f2str(
            conv_unit(pliq.IGProps.Cp, "J/molK", ene_per_mol_tempu), 6, lt=1e-2, gt=1e4
        )
        labels.append(Cps)
        liq_values.append(Cpl)
        vap_values.append(Cpl)

        dHIGs = "IG H [{0}]".format(ene_per_molu)
        dHIG = f2str(
            conv_unit(pliq.IGProps.H, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dHIGs)
        liq_values.append(dHIG)
        vap_values.append(dHIG)

        dSIGs = "IG S [{0}]".format(ene_per_mol_tempu)
        dSIG = f2str(
            conv_unit(pliq.IGProps.S, "J/molK", ene_per_mol_tempu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dSIGs)
        liq_values.append(dSIG)
        vap_values.append(dSIG)

        dGIGs = "IG G [{0}]".format(ene_per_molu)
        dGIG = f2str(
            conv_unit(pliq.IGProps.G, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dGIGs)
        liq_values.append(dGIG)
        vap_values.append(dGIG)

        dUIGs = "IG U [{0}]".format(ene_per_molu)
        dUIG = f2str(
            conv_unit(pliq.IGProps.U, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dUIGs)
        liq_values.append(dUIG)
        vap_values.append(dUIG)

        dAIGs = "IG A [{0}]".format(ene_per_molu)
        dAIG = f2str(
            conv_unit(pliq.IGProps.A, "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dAIGs)
        liq_values.append(dAIG)
        vap_values.append(dAIG)
    else:
        fs = "Fugacity [{0}]".format(Pu)
        fliq = f2str(conv_unit(pliq.Fugacity, "Pa", Pu), 8, lt=1e-2, gt=1e4)
        fvap = f2str(conv_unit(pvap.Fugacity, "Pa", Pu), 8, lt=1e-2, gt=1e4)
        labels.append(fs)
        liq_values.append(fliq)
        vap_values.append(fvap)
        # log += "Compound have no ideal properties (maybe it doesn't have ideal Cp parameters)\n"

    return labels, liq_values, vap_values
