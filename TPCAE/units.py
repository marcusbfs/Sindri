pressure_dict = {
    "bar": 1e5,
    "Pa": 1,
    "kPa": 1000,
    "atm": 101235.0,
    "psi": 6894.7572931783,
}

volume_dict = {
    "m3": 1,
    "L": 1e-3,
    "cm3": 1e6,
    "ft3": 1 / 35.3145,
}

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
    elif a in temperature_dict_to_K and b in temperature_dict_from_K:
        ans = temperature_dict_from_K[b](temperature_dict_to_K[a](number))
    else:
        raise ValueError
    return ans
