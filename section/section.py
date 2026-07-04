from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
from numpy import ndarray
from dataclasses import dataclass, field


@dataclass
class SectionState:
    
    sectionDeformationsCommitted: ndarray = field(default_factory=lambda: np.zeros((2,1)))
    sectionForcesCommitted: ndarray = field(default_factory=lambda: np.zeros((2,1)))

    sectionDeformationsTrial: ndarray = field(default_factory=lambda: np.zeros((2,1)))
    sectionForcesTrial: ndarray = field(default_factory=lambda: np.zeros((2,1)))

    def commit(self) -> None:
        self.sectionDeformationsCommitted = self.sectionDeformationsTrial.copy()
        self.sectionForcesCommitted = self.sectionForcesTrial.copy()

    def revert(self) -> None:
        self.sectionDeformationsTrial = self.sectionDeformationsCommitted.copy()
        self.sectionForcesTrial = self.sectionForcesCommitted.copy()


class Section(ABC):
    def __init__(self, id: str | int):
        self.id = id
        self.sectionState = SectionState()

    @abstractmethod
    def sectionStateDetermination(self,deformations: ndarray) -> None:
        ...

    @abstractmethod
    def getSectionForces(self) -> ndarray:
        ...

    @abstractmethod
    def getSectionStiffness(self) -> ndarray:
        ...

    @abstractmethod
    def getCopy(self):
        ...
