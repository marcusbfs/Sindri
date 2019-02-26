import numpy as np
import sympy as sp

from eos import EOS


class Mixture(EOS):
    def __init__(self, compounds, y, k, eos):

        EOS.__init__(self, compounds, y, k, eos)

        print(self.b)
        print(self.theta)
