import pytest
from tests.db_compound import methane
from TPCAE.antoineVP import antoineVP

A = methane["ANTOINE_A"]
B = methane["ANTOINE_B"]
C = methane["ANTOINE_C"]
Tmin = methane["Tmin_K"]
Tmax = methane["Tmax_K"]
T = 300


def test_antoineVP_returns_proper_Pvp_value():
    s = antoineVP(T, A, B, C, Tmin, Tmax)
    assert pytest.approx(s.Pvp, 1e-5) == 263.3184214


def test_antoineVP_returns_proper_out_of_lower_bound_msg():
    s = antoineVP(Tmin - 1, A, B, C, Tmin, Tmax)
    assert s.msg == 'T < Tmin'


def test_antoineVP_returns_proper_out_of_higher_bound_msg():
    s = antoineVP(Tmax + 1, A, B, C, Tmin, Tmax)
    assert s.msg == 'T > Tmax'
