def float2str(number, decimals, lt=None, gt=None):
    f = "{:." + str(decimals) + "f}"
    if lt and gt:
        if number < lt or number > gt:
            f = "{:." + str(decimals) + "e}"
    return f.format(number)
