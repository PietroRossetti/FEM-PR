from numpy import ndarray
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from node import Node
from section.section import Section
from geometricTransformation import GeometricTransformation

class ElementState:

    eleDispCommitted: ndarray
    eleForcesCommitted: ndarray

    eleDispTrial: ndarray
    eleForcesTrial: ndarray

    def commit(self):
        self.eleDispCommitted = self.eleDispTrial.copy()
        self.eleForcesCommitted = self.eleForcesTrial.copy()

    def revert(self):
        self.eleDispTrial = self.eleDispCommitted.copy()
        self.eleForcesTrial = self.eleForcesCommitted.copy()


class Element(ABC):
    def __init__(
            self,
            id: int|str,
            nodeI: Node,
            nodeJ: Node,
            section: Section,
            geomTransf: GeometricTransformation
    ) -> None:
        self.id = id
        self.nodeI = nodeI
        self.nodeJ = nodeJ
        self.geomTransf = geomTransf
        
    
    @abstractmethod
    def initialize(self):
        ...
    
    @abstractmethod
    def setTrialDisp(self):
        ...
    
    @abstractmethod
    def getEleForces(self) -> ndarray:
        ...
    
    @abstractmethod
    def getEleStiffness(self) -> ndarray:
        ...
    
    @abstractmethod
    def getDofIDs(self):
        return self.nodeI.getDofIDs() + self.nodeJ.getDofIDs()