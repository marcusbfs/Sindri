pressure_dict = {
    "bar": 1e5,
    "Pa": 1,
    "kPa": 1000,
    "atm": 101235.0,
    "psi": 6894.7572931783,
}

mol_dict = {"mol": 1, "kmol": 1000}

mass_dict = {"kg": 1, "g": 1e-3}

volume_dict = {"m3": 1, "L": 1e-3, "cm3": 1 / 100 ** 3, "ft3": 1 / 35.3145}


temperature_dict_to_K = {
    "K": lambda K: K,
    "ºC": lambda C: C + 273.15,
    "ºF": lambda F: (F - 32.0) / 1.8 + 273.15,
    "ºR": lambda R: R * 5 / 9,
}

temperature_dict_from_K = {
    "K": lambda K: K,
    "ºC": lambda K: K - 273.15,
    "ºF": lambda K: (K - 273.15) * 1.8 + 32.0,
    "ºR": lambda K: K * 9 / 5,
}

temperature_options = list(temperature_dict_to_K.keys())
pressure_options = list(pressure_dict.keys())
volume_options = list(volume_dict.keys())
mass_options = list(mass_dict.keys())
mol_options = list(mol_dict.keys())

# derivative units


def cbu(n, a, b):
    if a in pressure_dict and b in pressure_dict:
        ans = n * pressure_dict[a] / pressure_dict[b]
    elif a in volume_dict and b in volume_dict:
        ans = n * volume_dict[a] / volume_dict[b]
    elif a in temperature_dict_to_K and b in temperature_dict_from_K:
        ans = temperature_dict_from_K[b](temperature_dict_to_K[a](n))
    elif a in mass_dict and b in mass_dict:
        ans = n * mass_dict[a] / mass_dict[b]
    elif a in mol_dict and b in mol_dict:
        ans = n * mol_dict[a] / mol_dict[b]
    return ans


molar_vol_dict = {
    "m3/mol": 1,
    "m3/kmol": 1 / cbu(1, "kmol", "mol"),
    "cm3/mol": cbu(1, "cm3", "m3"),
    "cm3/kmol": cbu(1, "cm3", "m3") / cbu(1, "kmol", "mol"),
}

energy_dict = {"J": 1, "kJ": 1000, "cal": 4.18401, "kcal": 4184.01, "BTU": 1055.06}

energy_per_mol_dict = {
    "J/mol": 1,
    "kJ/mol": 1000,
    "cal/mol": 4.18401,
    "kcal/mol": 4184.01,
    "BTU/mol": 1055.06,
    "J/kmol": 1 / 1000,
    "kJ/kmol": 1,
    "cal/kmol": 4.18401 / 1000,
    "kcal/kmol": 4184.01 / 1e3,
    "BTU/kmol": 1055.06 / 1e3,
}

density_dict = {"kg/m3": 1, "g/cm3": cbu(1, "g", "kg") / cbu(1, "cm3", "m3")}

density_options = list(density_dict.keys())
molar_vol_options = list(molar_vol_dict.keys())
energy_options = list(energy_dict.keys())
energy_per_mol_options = list(energy_per_mol_dict.keys())


# conversion functions


def convert_to_SI(unit, number, s):
    try:
        if unit == "pressure":
            return conv_unit(number, s, "Pa")
        elif unit == "temperature":
            return conv_unit(number, s, "K")
        else:
            raise Exception("couldnt identify unit")
    except:
        raise Exception("error converting units")


def conv_unit(number, a, b):
    if a in pressure_dict and b in pressure_dict:
        ans = number * pressure_dict[a] / pressure_dict[b]
    elif a in volume_dict and b in volume_dict:
        ans = number * volume_dict[a] / volume_dict[b]
    elif a in molar_vol_dict and b in molar_vol_dict:
        ans = number * molar_vol_dict[a] / molar_vol_dict[b]
    elif a in mass_dict and b in mass_dict:
        ans = number * mass_dict[a] / mass_dict[b]
    elif a in density_dict and b in density_dict:
        ans = number * density_dict[a] / density_dict[b]
    elif a in energy_dict and b in energy_dict:
        ans = number * energy_dict[a] / energy_dict[b]
    elif a in energy_per_mol_dict and b in energy_per_mol_dict:
        ans = number * energy_per_mol_dict[a] / energy_per_mol_dict[b]
    elif a in temperature_dict_to_K and b in temperature_dict_from_K:
        ans = temperature_dict_from_K[b](temperature_dict_to_K[a](number))
    else:
        raise ValueError
    return ans
