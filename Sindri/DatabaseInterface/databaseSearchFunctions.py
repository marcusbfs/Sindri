def getQueryBySearchNameFormulaOrCas(s: str) -> str:
    query = (
        "SELECT * FROM database WHERE Name LIKE '%"
        + s
        + "%'"
        + " OR Formula LIKE '%"
        + s
        + "%'"
        + " OR `CAS #` LIKE '%"
        + s
        + "%' ORDER BY (Name = '"
        + s
        + "' OR Formula = '"
        + s
        + "' OR `CAS #` = '"
        + s
        + "') DESC, length(Name)"
    )
    return query
