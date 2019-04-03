import abc
from EOSParametersBehavior.ParametersBehaviorInterface import (
    BiBehavior,
    DeltaiBehavior,
    ThetaiBehavior,
    EpsiloniBehavior,
)
import numpy as np


class MixtureRuleBehavior:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        pass

    @abc.abstractmethod
    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        pass

    @abc.abstractmethod
    def thetam(self, y, T: float, thetaib: ThetaiBehavior, substances, k) -> float:
        pass

    @abc.abstractmethod
    def diffThetam(
        self, i: int, y, T: float, thetaib: ThetaiBehavior, substances, k
    ) -> float:
        pass


class BMixtureRuleBehavior:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def bm(self, y, T: float, bib: BiBehavior, substances) -> float:
        pass

    @abc.abstractmethod
    def diffBm(self, i: int, y, T: float, bib: BiBehavior, substances) -> float:
        pass


class ThetaMixtureRuleBehavior:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def thetam(self, y, T: float, thetaib: ThetaiBehavior, substances, k) -> float:
        pass

    @abc.abstractmethod
    def diffThetam(
        self, i: int, y, T: float, thetaib: ThetaiBehavior, substances, k
    ) -> float:
        pass


class DeltaMixtureRuleBehavior:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deltam(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        pass

    @abc.abstractmethod
    def diffDeltam(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: MixtureRuleBehavior,
        substances,
    ) -> float:
        pass


class EpsilonMixtureRuleBehavior:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def epsilonm(
        self, y, T: float, bib: BiBehavior, bmb: MixtureRuleBehavior, substances
    ) -> float:
        pass

    @abc.abstractmethod
    def diffEpsilonm(
        self,
        i: int,
        y,
        T: float,
        bib: BiBehavior,
        bmb: MixtureRuleBehavior,
        substances,
    ) -> float:
        pass
