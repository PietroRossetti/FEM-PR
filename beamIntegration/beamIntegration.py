from __future__ import annotations

from abc import ABC, abstractmethod

from section.section import Section


class BeamIntegration(ABC):
    """
    Base class for beam integration rules.

    It stores the integration locations, weights, and a reference section.
    Elements are responsible for creating the section copies they need.
    """

    def __init__(
            self,
            id: str | int,
            nIP: int,
            section: Section
    ) -> None:
        if type(nIP) is not int:
            raise ValueError("number of integration points must be an integer")
        if nIP <= 0:
            raise ValueError("number of integration points must be positive")

        self.id = id
        self.nIP = nIP
        self.theSection = section

        self.position, self.weight = self._get_rule(nIP)


    @abstractmethod
    def _get_rule(self, nIP: int) -> tuple[list[float], list[float]]:
        ...

    @abstractmethod
    def getCopy(self) -> BeamIntegration:
        ...

    def getTheSection(self) -> Section:
        return self.theSection

    @abstractmethod
    def getLocations(self, L:float) -> list[float]:
        return ...

    @abstractmethod
    def getWeights(self, L:float) -> list[float]:
        return ...
