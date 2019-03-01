from utils import f2str
from units import pressure_options, temperature_options, volume_options, conv_unit
from IdealGasPropertiesPureSubstance import state_options


def format_reports(prop, **units):

    state = prop.state
    log = prop.log
    has_ig = True if prop.ideal is not None else False

    # units
    Tu = units["T"] if "T" in units else "K"
    Vu = units["V"] if "V" in units else "m3/mol"
    Pu = units["P"] if "P" in units else "Pa"
    rhou = units["rho"] if "rho" in units else "kg/m3"
    ene_per_molu = units["energy_per_mol"] if "energy_per_mol" in units else "J/mol"
    ene_per_mol_tempu = (
        units["energy_per_mol_temp"] if "energy_per_mol_temp" in units else "J/molK"
    )

    reportret = "fluid state: {0}\n".format(state)

    def formatter(info, lval, vval):
        return "{0:<25}\t{1:>20}\t{2:>20}\n".format(info, lval, vval)

    reportret += formatter("Property", "Liquid", "Vapor")

    # Z, V and density
    Zl = f2str(prop.liq["Z"], 8, lt=1e-1)
    Zv = f2str(prop.vap["Z"], 8, lt=1e-1)

    Vs = "V [{0}]".format(Vu)
    Vl = f2str(conv_unit(prop.liq["V"], "m3/mol", Vu), 8, lt=1e-2, gt=1e4)
    Vv = f2str(conv_unit(prop.vap["V"], "m3/mol", Vu), 8, lt=1e-2, gt=1e4)

    rhos = "Density [{0}]".format(rhou)
    rhol = f2str(conv_unit(prop.liq["rho"], "kg/m3", rhou), 8, lt=1e-2, gt=1e4)
    rhov = f2str(conv_unit(prop.vap["rho"], "kg/m3", rhou), 8, lt=1e-2, gt=1e4)

    reportret += formatter("Z", Zl, Zv)
    reportret += formatter(Vs, Vl, Vv)
    reportret += formatter(rhos, rhol, rhov)

    # Vapor pressure

    if prop.Pvp != 0:
        Pvpeoss = "Vap. P (EOS) [{0}]".format(Pu)
        Pvpeosl = f2str(conv_unit(prop.Pvp["EOS"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        Pvpeosv = f2str(conv_unit(prop.Pvp["EOS"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        reportret += formatter(Pvpeoss, Pvpeosl, Pvpeosv)

        PvpAWs = "Vap. P (Ambrose-Walton) [{0}]".format(Pu)
        PvpAWl = f2str(
            conv_unit(prop.Pvp["AmbroseWalton"], "Pa", Pu), 8, lt=1e-2, gt=1e4
        )
        PvpAWv = f2str(
            conv_unit(prop.Pvp["AmbroseWalton"], "Pa", Pu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(PvpAWs, PvpAWl, PvpAWv)

        PvpLKs = "Vap. P (Lee-Kesler) [{0}]".format(Pu)
        PvpLKl = f2str(conv_unit(prop.Pvp["LeeKesler"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        PvpLKv = f2str(conv_unit(prop.Pvp["LeeKesler"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        reportret += formatter(PvpLKs, PvpLKl, PvpLKv)

        if prop.Pvp["Antoine"] is not None:
            PvpAntoines = "Vap. P (Antoine) [{0}]".format(Pu)
            PvpAntoinel = f2str(
                conv_unit(prop.Pvp["Antoine"].Pvp, "Pa", Pu), 8, lt=1e-2, gt=1e4
            )
            PvpAntoinev = f2str(
                conv_unit(prop.Pvp["Antoine"].Pvp, "Pa", Pu), 8, lt=1e-2, gt=1e4
            )
            reportret += formatter(PvpAntoines, PvpAntoinel, PvpAntoinev)

    # ideal property (if any)
    if has_ig:

        # Cp
        Cps = "Cp [{0}]".format(ene_per_mol_tempu)
        Cpl = f2str(prop.ideal["Cp"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(Cps, Cpl, Cpl)

        # Ideal properties
        dHIGs = "IG H [{0}]".format(ene_per_molu)
        dHIG = f2str(
            conv_unit(prop.ideal["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dHIGs, dHIG, dHIG)

        dSIGs = "IG S [{0}]".format(ene_per_mol_tempu)
        dSIG = f2str(prop.ideal["dS"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(dSIGs, dSIG, dSIG)

        dGIGs = "IG G [{0}]".format(ene_per_molu)
        dGIG = f2str(
            conv_unit(prop.ideal["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dGIGs, dGIG, dGIG)

        dUIGs = "IG U [{0}]".format(ene_per_molu)
        dUIG = f2str(
            conv_unit(prop.ideal["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dUIGs, dUIG, dUIG)

        dAIGs = "IG A [{0}]".format(ene_per_molu)
        dAIG = f2str(
            conv_unit(prop.ideal["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dAIGs, dAIG, dAIG)

        # real properties
        dHs = "H [{0}]".format(ene_per_molu)
        dHliq = f2str(
            conv_unit(prop.liq["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dHvap = f2str(
            conv_unit(prop.vap["dH"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dHs, dHliq, dHvap)

        dSs = "S [{0}]".format(ene_per_mol_tempu)
        dSliq = f2str(prop.liq["dS"], 8, lt=1e-2, gt=1e4)
        dSvap = f2str(prop.vap["dS"], 8, lt=1e-2, gt=1e4)
        reportret += formatter(dSs, dSliq, dSvap)

        dGs = "G [{0}]".format(ene_per_molu)
        dGliq = f2str(
            conv_unit(prop.liq["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dGvap = f2str(
            conv_unit(prop.vap["dG"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dGs, dGliq, dGvap)

        dUs = "U [{0}]".format(ene_per_molu)
        dUliq = f2str(
            conv_unit(prop.liq["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dUvap = f2str(
            conv_unit(prop.vap["dU"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dUs, dUliq, dUvap)

        dAs = "A [{0}]".format(ene_per_molu)
        dAliq = f2str(
            conv_unit(prop.liq["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        dAvap = f2str(
            conv_unit(prop.vap["dA"], "J/mol", ene_per_molu), 8, lt=1e-2, gt=1e4
        )
        reportret += formatter(dAs, dAliq, dAvap)

    else:
        reportret += "Compound has no Cp equation parameters\n"
        log += "Compound has no Cp equation parameters\n"

    # fugacity
    fs = "fugacity [{0}]".format(Pu)
    fliq = f2str(conv_unit(prop.liq["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
    fvap = f2str(conv_unit(prop.vap["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
    reportret += formatter(fs, fliq, fvap)

    return reportret, log


def tablewidget_vap_liq_reports(prop, **units):

    labels = []
    liq_values = []
    vap_values = []

    state = prop.state
    log = prop.log
    has_ig = True if prop.ideal is not None else False

    # units
    Tu = units["T"] if "T" in units else "K"
    Vu = units["V"] if "V" in units else "m3/mol"
    Pu = units["P"] if "P" in units else "Pa"
    rhou = units["rho"] if "rho" in units else "kg/m3"
    ene_per_molu = units["energy_per_mol"] if "energy_per_mol" in units else "J/mol"
    ene_per_mol_tempu = (
        units["energy_per_mol_temp"] if "energy_per_mol_temp" in units else "J/molK"
    )

    def formatter(info, lval, vval):
        return "{0:<21}\t{1:>20}\t{2:>20}\n".format(info, lval, vval)

    # Z, V and density
    Zl = f2str(prop.liq["Z"], 6, lt=1e-1)
    Zv = f2str(prop.vap["Z"], 6, lt=1e-1)
    labels.append("Z")
    liq_values.append(Zl)
    vap_values.append(Zv)

    Vs = "V [{0}]".format(Vu)
    Vl = f2str(conv_unit(prop.liq["V"], "m3/mol", Vu), 6, lt=1e-2, gt=1e4)
    Vv = f2str(conv_unit(prop.vap["V"], "m3/mol", Vu), 6, lt=1e-2, gt=1e4)
    labels.append(Vs)
    liq_values.append(Vl)
    vap_values.append(Vv)

    rhos = "Density [{0}]".format(rhou)
    rhol = f2str(conv_unit(prop.liq["rho"], "kg/m3", rhou), 6, lt=1e-2, gt=1e4)
    rhov = f2str(conv_unit(prop.vap["rho"], "kg/m3", rhou), 6, lt=1e-2, gt=1e4)
    labels.append(rhos)
    liq_values.append(rhol)
    vap_values.append(rhov)

    # Vapor pressure

    if prop.Pvp != 0:
        Pvpeoss = "Vap. P (EOS) [{0}]".format(Pu)
        Pvpeosl = f2str(conv_unit(prop.Pvp["EOS"], "Pa", Pu), 6, lt=1e-2, gt=1e4)
        Pvpeosv = f2str(conv_unit(prop.Pvp["EOS"], "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(Pvpeoss)
        liq_values.append(Pvpeosl)
        vap_values.append(Pvpeosv)

        PvpAWs = "Vap. P (Ambrose-Walton) [{0}]".format(Pu)
        PvpAWl = f2str(
            conv_unit(prop.Pvp["AmbroseWalton"], "Pa", Pu), 6, lt=1e-2, gt=1e4
        )
        PvpAWv = f2str(
            conv_unit(prop.Pvp["AmbroseWalton"], "Pa", Pu), 6, lt=1e-2, gt=1e4
        )
        labels.append(PvpAWs)
        liq_values.append(PvpAWl)
        vap_values.append(PvpAWv)

        PvpLKs = "Vap. P (Lee-Kesler) [{0}]".format(Pu)
        PvpLKl = f2str(conv_unit(prop.Pvp["LeeKesler"], "Pa", Pu), 6, lt=1e-2, gt=1e4)
        PvpLKv = f2str(conv_unit(prop.Pvp["LeeKesler"], "Pa", Pu), 6, lt=1e-2, gt=1e4)
        labels.append(PvpLKs)
        liq_values.append(PvpLKl)
        vap_values.append(PvpLKv)

        if prop.Pvp["Antoine"] is not None:
            PvpAntoines = "Vap. P (Antoine) [{0}]".format(Pu)
            PvpAntoinel = f2str(
                conv_unit(prop.Pvp["Antoine"].Pvp, "Pa", Pu), 6, lt=1e-2, gt=1e4
            )
            PvpAntoinev = f2str(
                conv_unit(prop.Pvp["Antoine"].Pvp, "Pa", Pu), 6, lt=1e-2, gt=1e4
            )
            labels.append(PvpAntoines)
            liq_values.append(PvpAntoinel)
            vap_values.append(PvpAntoinev)

    # ideal property (if any)
    if has_ig:

        # Cp
        Cps = "Cp [{0}]".format(ene_per_mol_tempu)
        Cpl = f2str(prop.ideal["Cp"], 6, lt=1e-2, gt=1e4)
        labels.append(Cps)
        liq_values.append(Cpl)
        vap_values.append(Cpl)

        # real properties
        dHs = "H [{0}]".format(ene_per_molu)
        dHliq = f2str(
            conv_unit(prop.liq["dH"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dHvap = f2str(
            conv_unit(prop.vap["dH"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dHs)
        liq_values.append(dHliq)
        vap_values.append(dHvap)

        dSs = "S [{0}]".format(ene_per_mol_tempu)
        dSliq = f2str(prop.liq["dS"], 6, lt=1e-2, gt=1e4)
        dSvap = f2str(prop.vap["dS"], 6, lt=1e-2, gt=1e4)
        labels.append(dSs)
        liq_values.append(dSliq)
        vap_values.append(dSvap)

        dGs = "G [{0}]".format(ene_per_molu)
        dGliq = f2str(
            conv_unit(prop.liq["dG"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dGvap = f2str(
            conv_unit(prop.vap["dG"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dGs)
        liq_values.append(dGliq)
        vap_values.append(dGvap)

        dUs = "U [{0}]".format(ene_per_molu)
        dUliq = f2str(
            conv_unit(prop.liq["dU"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dUvap = f2str(
            conv_unit(prop.vap["dU"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dUs)
        liq_values.append(dUliq)
        vap_values.append(dUvap)

        dAs = "A [{0}]".format(ene_per_molu)
        dAliq = f2str(
            conv_unit(prop.liq["dA"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        dAvap = f2str(
            conv_unit(prop.vap["dA"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dAs)
        liq_values.append(dAliq)
        vap_values.append(dAvap)

        # fugacity
        fs = "Fugacity [{0}]".format(Pu)
        fliq = f2str(conv_unit(prop.liq["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        fvap = f2str(conv_unit(prop.vap["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        labels.append(fs)
        liq_values.append(fliq)
        vap_values.append(fvap)

        # Ideal properties
        dHIGs = "IG H [{0}]".format(ene_per_molu)
        dHIG = f2str(
            conv_unit(prop.ideal["dH"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dHIGs)
        liq_values.append(dHIG)
        vap_values.append(dHIG)

        dSIGs = "IG S [{0}]".format(ene_per_mol_tempu)
        dSIG = f2str(prop.ideal["dS"], 6, lt=1e-2, gt=1e4)
        labels.append(dSIGs)
        liq_values.append(dSIG)
        vap_values.append(dSIG)

        dGIGs = "IG G [{0}]".format(ene_per_molu)
        dGIG = f2str(
            conv_unit(prop.ideal["dG"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dGIGs)
        liq_values.append(dGIG)
        vap_values.append(dGIG)

        dUIGs = "IG U [{0}]".format(ene_per_molu)
        dUIG = f2str(
            conv_unit(prop.ideal["dU"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dUIGs)
        liq_values.append(dUIG)
        vap_values.append(dUIG)

        dAIGs = "IG A [{0}]".format(ene_per_molu)
        dAIG = f2str(
            conv_unit(prop.ideal["dA"], "J/mol", ene_per_molu), 6, lt=1e-2, gt=1e4
        )
        labels.append(dAIGs)
        liq_values.append(dAIG)
        vap_values.append(dAIG)
    else:
        fs = "Fugacity [{0}]".format(Pu)
        fliq = f2str(conv_unit(prop.liq["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        fvap = f2str(conv_unit(prop.vap["f"], "Pa", Pu), 8, lt=1e-2, gt=1e4)
        labels.append(fs)
        liq_values.append(fliq)
        vap_values.append(fvap)
        log += "Compound have no ideal properties (maybe it doesn't have ideal Cp parameters)\n"

    return labels, liq_values, vap_values
