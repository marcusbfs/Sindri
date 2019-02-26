from TPCAE.mixtures import *
from TPCAE.eos import *
from TPCAE.db_utils import get_compound_properties

pentane = get_compound_properties("pentane", "C5H12")
hexane = get_compound_properties("hexane", "C6H14")

mix = [pentane, hexane]
y = [0.5, 0.5]
k = [[0.0, 0.01], [0.01, 0.0]]
# k = [[0.01, .0],
#      [.0,0.01]]
eos = "peng_and_robinson_1976"

m = Mixture(mix, y, k, eos)


def test_check_volume_function():
    ret = m.return_Z_given_PT(1e5, 150)
    print(ret)
    assert 0
