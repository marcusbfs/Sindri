from TPCAE.db_utils import get_compound_properties
from tests.db_compound import methane

name = methane["Name"]
formula = methane["Formula"]


# TODO how to test it?
# def test_get_compound_properties_return_correct_dictionary():
#     assert methane == get_compound_properties(name, formula)
