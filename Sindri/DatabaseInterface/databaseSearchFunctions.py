def getQueryBySearchNameFormulaOrCas(s: str) -> str:
    table_name = "v_all_properties_including_correlations s"
    table_name += " INNER JOIN substance sub ON sub.cas=s.cas LEFT JOIN substance_name_aliases a on sub.substance_id=a.substance_id"
    query = """SELECT DISTINCT s.formula, s.name, s.cas, s.molar_weigth,
               s.tfp_k, s.tb_k, s.tc_k, s.pc_bar, s.vc_cm3_per_mol, s.zc, s.omega,
               s.cp_trange, s.cp_a0, s.cp_a1, s.cp_a2, s.cp_a3, s.cp_a4, s.cpig, s.cpliq,
               s.antoine_a, s.antoine_b, s.antoine_c, s.pvpmin_bar, s.tmin_k, s.pvpmax_bar, s.tmax_k
               FROM {0}
               WHERE s.name LIKE '%{1}%'
               OR s.formula LIKE '%{1}%'
               OR s.cas LIKE '%{1}%'
               OR a.alias LIKE '%{1}%'
               ORDER BY (s.name='{1}') DESC, length(s.name)""".format(
        table_name, s
    )
    return query
