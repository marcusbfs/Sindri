def getQueryBySearchNameFormulaOrCas(s: str) -> str:
    # join = "substance s LEFT JOIN cp_correlations c ON s.substance_id = c.substance_id LEFT JOIN antoine_correlations a ON a.substance_id = s.substance_id"
    table_name = "v_all_properties_including_correlations"
    query = (
        "SELECT * FROM "
        + table_name
        + " WHERE name LIKE '%"
        + s
        + "%'"
        + " OR formula LIKE '%"
        + s
        + "%'"
        + " OR cas LIKE '%"
        + s
        + "%' ORDER BY (name = '"
        + s
        + "' OR formula = '"
        + s
        + "' OR cas = '"
        + s
        + "') DESC, length(name)"
    )
    return query
