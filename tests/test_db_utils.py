from TPCAE.db_utils import get_compound_properties
from tests.db_compound import methane

name = methane["Name"]
formula = methane["Formula"]


def test_get_compound_properties_return_correct_dictionary():
    methane = get_compound_properties(name, formula)
    print(methane.getName())
    print(methane.getFormula())
    print(methane.getCpCoeffs())
