def f2str(number, decimals, lt=None, gt=None):
    f = "{:." + str(decimals) + "f}"
    if lt and gt:
        if abs(number) < lt or abs(number) > gt:
            f = "{:." + str(decimals) + "e}"
    return f.format(number)
