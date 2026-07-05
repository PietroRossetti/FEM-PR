from __future__ import annotations
from abc import ABC, abstractmethod
from numpy import ndarray


class Section(ABC):
    def __init__(self, id: str | int):
        self.id = id
        #self.sectionState = SectionState()
        
    # -----------------------------------------------------
    #       SECTION STATE DETERMINATION - start
    # -----------------------------------------------------
    @abstractmethod
    def setSectionDeformations(self, e: ndarray) -> None:
        '''
        e: section deformations {eps, curvature}^t
        '''
        ...

    @abstractmethod
    def getSectionForces(self) -> ndarray:
        ...

    @abstractmethod
    def getSectionStiffness(self) -> ndarray:
        ...
    # -----------------------------------------------------
    #       SECTION STATE DETERMINATION - end
    # -----------------------------------------------------

    @abstractmethod
    def getCopy(self):
        ...