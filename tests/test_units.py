from TPCAE.units import conv_unit, convert_to_SI

import pytest


# temperatures conversions

def test_temperatures_C_to_K():
    assert conv_unit(25, "ºC", "K") == 298.15


def test_temperatures_K_to_C():
    assert conv_unit(298.15, "K", "ºC") == 25


def test_temperatures_K_to_F():
    assert pytest.approx(conv_unit(300, "K", "ºF"), 1e-5) == 80.33


def test_temperatures_F_to_K():
    assert pytest.approx(conv_unit(80.33, "ºF", "K"), 1e-5) == 300


def test_temperatures_K_to_R():
    assert pytest.approx(conv_unit(300, "K", "ºR"), 1e-5) == 540


def test_temperatures_R_to_K():
    assert pytest.approx(conv_unit(540, "ºR", "K"), 1e-5) == 300

# pressure conversions
