# Pressure
Pa_to_Pa = 1.0

atm_to_bar = 1.01325
bar_to_atm = 1.0 / atm_to_bar

Pa_to_bar = 1e-5
bar_to_Pa = 1.0 / Pa_to_bar

atm_to_Pa = 101235.0
Pa_to_atm = 1.0 / atm_to_Pa

kPa_to_Pa = 1000.
Pa_to_kPa = 1. / kPa_to_Pa


# Temperature
def K_to_K(k): return k


def K_to_C(K): return K - 273.15


def C_to_K(c): return c + 273.15


def F_to_C(f): return (f - 32) / 1.8


def C_to_F(c): return c * 1.8 + 32


def F_to_K(f): return C_to_K(F_to_C(f))


def K_to_F(K): return C_to_F(K_to_C(K))


pressure_dict = {
    "Pa": 1,
    "kPa": 1000,
    "bar": 1e5,
    "atm": 101235.0,
    "psi": 6894.7572931783,
}

volume_dict = {
    "m3": 1,
    "L": 1000,
    "cm3": 1e6,
    "ft3": 35.3145,
}

temperature_dict_to_K = {
    "K": lambda x: x,
    "ºC": lambda x: x + 273.15,
    "ºF": lambda x: F_to_K(x),
    "ºR": lambda x: x * 5 / 9,
}

temperature_dict_from_K = {
    "K": lambda x: x,
    "ºC": lambda x: x - 273.15,
    "ºF": lambda x: K_to_F(x),
    "ºR": lambda x: x * 9 / 5,
}

temperature_options = list(temperature_dict_to_K.keys())
pressure_options = list(pressure_dict.keys())
volume_options = list(volume_dict.keys())


def convert_to_SI(unit, number, s):
    try:
        if unit == "pressure":
            # c = s + "_to_Pa"
            # e = "ans = " + str(number) + " * " + c
            # exec(e, globals(), globals())
            # return ans
            return conv_unit(number, s, "Pa")
        elif unit == "temperature":
            # c = s.replace("º", "") + "_to_K"
            # e = "ans = " + c + "(" + str(number) + ")"
            # exec(e, globals(), globals())
            # return ans
            return conv_unit(number, s, "K")
        else:
            raise Exception("couldnt identify unit")
    except:
        raise Exception("error converting units")


def conv_unit(number, a, b):
    if a in pressure_dict and b in pressure_dict:
        ans = number * pressure_dict[a] / pressure_dict[b]
        return ans
    elif a in temperature_dict_to_K and b in temperature_dict_from_K:
        ans = temperature_dict_from_K[b](temperature_dict_to_K[a](number))
    else:
        raise ValueError
    return ans


if __name__ == "__main__":
    # c = 20
    # print(C_to_K(c))
    # print(C_to_F(c))
    # print(F_to_K(68))
    # print(convert_to_SI("pressure", 1, "bar"))
    # print(convert_to_SI("temperature", 20, "ºC"))
    print(conv_unit(20, "ºC", "ºR"))
    # a = conv_unit(1, "bar", "Pa")
    # print(a)
    print(pressure_options)
    print(temperature_options)
