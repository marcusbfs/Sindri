from TPCAE.units import conv_unit, convert_to_SI

import pytest


# temperatures conversions
class TestTemperaturesConversions(object):
    def test_temperatures_have_the_same_number_of_conversions_from_and_to_Kelvin(self):
        from TPCAE.units import (
            temperature_dict_to_K,
            temperature_options,
            temperature_dict_from_K,
        )

        assert temperature_dict_from_K.keys() == temperature_dict_to_K.keys()
        assert list(temperature_dict_from_K.keys()) == temperature_options

    def test_temperatures_K_to_K(self):
        assert conv_unit(25, "K", "K") == 25

    def test_temperatures_C_to_K(self):
        assert conv_unit(25, "ºC", "K") == 298.15

    def test_temperatures_K_to_C(self):
        assert conv_unit(298.15, "K", "ºC") == 25

    def test_temperatures_K_to_F(self):
        assert pytest.approx(conv_unit(300, "K", "ºF"), 1e-5) == 80.33

    def test_temperatures_F_to_K(self):
        assert pytest.approx(conv_unit(80.33, "ºF", "K"), 1e-5) == 300

    def test_temperatures_K_to_R(self):
        assert pytest.approx(conv_unit(300, "K", "ºR"), 1e-5) == 540

    def test_temperatures_R_to_K(self):
        assert pytest.approx(conv_unit(540, "ºR", "K"), 1e-5) == 300


# pressure conversions
class TestPressuresConversions(object):
    def test_pressures_Pa_to_Pa(self):
        assert pytest.approx(conv_unit(1, "Pa", "Pa"), 1e-3) == 1

    def test_pressures_Pa_to_bar(self):
        assert pytest.approx(conv_unit(1, "Pa", "bar"), 1e-3) == 1e-5

    def test_pressures_bar_to_Pa(self):
        assert pytest.approx(conv_unit(1, "bar", "Pa"), 1e-3) == 1e5

    def test_pressures_Pa_to_atm(self):
        assert pytest.approx(conv_unit(1, "Pa", "atm"), 1e-3) == 1 / 101325

    def test_pressures_atm_to_Pa(self):
        assert pytest.approx(conv_unit(1, "atm", "Pa"), 1e-3) == 101325

    def test_pressures_Pa_to_psi(self):
        assert pytest.approx(conv_unit(1, "Pa", "psi"), 1e-3) == 1 / 6894.7572931783

    def test_pressures_psi_to_Pa(self):
        assert pytest.approx(conv_unit(1, "psi", "Pa"), 1e-3) == 6894.7572931783

    def test_pressures_Pa_to_kPa(self):
        assert pytest.approx(conv_unit(1, "Pa", "kPa"), 1e-3) == 1e-3

    def test_pressures_kPa_to_Pa(self):
        assert pytest.approx(conv_unit(1, "kPa", "Pa"), 1e-3) == 1e3


class TestVolumesConversions(object):
    def test_volumes_m3_to_m3(self):
        assert pytest.approx(conv_unit(1, "m3", "m3"), 1e-3) == 1

    def test_volumes_cm3_to_m3(self):
        assert pytest.approx(conv_unit(1, "cm3", "m3"), 1e-3) == 1 / 100 ** 3

    def test_volumes_m3_to_cm3(self):
        assert pytest.approx(conv_unit(1, "m3", "cm3"), 1e-3) == 100 ** 3

    def test_volumes_L_to_m3(self):
        assert pytest.approx(conv_unit(1, "L", "m3"), 1e-3) == 1 / 1000

    def test_volumes_m3_to_ft3(self):
        assert pytest.approx(conv_unit(1, "m3", "ft3"), 1e-3) == 1000

    def test_volumes_ft3_to_m3(self):
        assert pytest.approx(conv_unit(1, "ft3", "m3"), 1e-3) == 0.0283168

    def test_volumes_m3_to_ft3(self):
        assert pytest.approx(conv_unit(1, "m3", "ft3"), 1e-3) == 1 / 0.0283168
