def f2str(number, decimals, lt=None, gt=None):
    f = "{:." + str(decimals) + "f}"
    if lt is not None and gt is not None:
        if abs(number) < lt or abs(number) > gt:
            f = "{:." + str(decimals) + "e}"
    elif lt is not None:
        if abs(number < lt):
            f = "{:." + str(decimals) + "e}"
    elif gt is not None:
        if abs(number > gt):
            f = "{:." + str(decimals) + "e}"
    return f.format(number)
