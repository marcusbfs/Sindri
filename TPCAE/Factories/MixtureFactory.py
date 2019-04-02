from compounds import SubstanceProp


def createMix(names, formulas):
    assert len(names) == len(formulas)
    n = len(names)
    subs = []

    for i in range(n):
        subs.append( SubstanceProp(names[i], formulas[i]))

    return subs
