def f2str(number, decimals, lt=None, gt=None):
    """
    Formats a number to be displayed


    Parameters
    ----------
    number : float
        number to be formatted
    decimals : float
        decimal points to be displayed
    lt : float or None
    gt : float or None

    Returns
    -------
    f : str
        formatted number to be displayed

    """
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
