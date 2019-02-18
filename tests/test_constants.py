import pytest
from TPCAE.constants import R_IG


def test_R_IG_constant_value_in_SI_system():
    assert R_IG == 8.314462175
