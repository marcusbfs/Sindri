import abc
import compounds
import numpy as np


class BiBehavior:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getBi(self, i: int, T: float, substances) -> float:
        pass


class ThetaiBehavior:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getThetai(self, i: int, T: float, substances) -> float:
        pass


class DeltaiBehavior:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getDeltai(self, b: float) -> float:
        pass


class EpsiloniBehavior:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getEpsiloni(self, b: float) -> float:
        pass
