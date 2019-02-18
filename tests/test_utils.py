from TPCAE.utils import f2str


def test_f2str_return_correct_string():
    assert f2str(0.666666666, 2) == '0.67'
