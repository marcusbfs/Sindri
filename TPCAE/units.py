# Pressure
Pa_to_Pa = 1.0

atm_to_bar = 1.01325
bar_to_atm = 1.0 / atm_to_bar

Pa_to_bar = 1e-5
bar_to_Pa = 1.0 / Pa_to_bar

atm_to_Pa = 101235.0
Pa_to_atm = 1.0 / atm_to_Pa


# Temperature
def K_to_K(k): return k


def K_to_C(K): return K - 273.15


def C_to_K(c): return c + 273.15


def F_to_C(f): return (f - 32) / 1.8


def C_to_F(c): return c * 1.8 + 32


def F_to_K(f): return C_to_K(F_to_C(f))


def K_to_F(K): return C_to_F(K_to_C(K))


def convert_to_SI(unit, number, s):
    try:
        if unit == "pressure":
            c = s + "_to_Pa"
            e = "ans = " + str(number) + " * " + c
            exec(e, globals(), globals())
            return ans
        elif unit == "temperature":
            c = s.replace("º", "") + "_to_K"
            e = "ans = " + c + "(" + str(number) + ")"
            exec(e, globals(), globals())
            return ans
        else:
            raise Exception("couldnt identify unit")
    except:
        raise Exception("error converting units")


if __name__ == "__main__":
    # c = 20
    # print(C_to_K(c))
    # print(C_to_F(c))
    # print(F_to_K(68))
    print(convert_to_SI("pressure", 1, "bar"))
    print(convert_to_SI("temperature", 20, "ºC"))
