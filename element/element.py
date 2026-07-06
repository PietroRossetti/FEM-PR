from numpy import ndarray
from abc import ABC, abstractmethod
from node import Node
from beamIntegration.beamIntegration import BeamIntegration
from geometricTransformation import GeometricTransformation


class Element(ABC):
    def __init__(
            self,
            id: int|str,
            nodeI: Node,
            nodeJ: Node,
            beamIntegration: BeamIntegration,
            geomTransf: GeometricTransformation
    ) -> None:
        self.id = id
        self.nodeI = nodeI
        self.nodeJ = nodeJ
        self.beamIntegration = beamIntegration
        self.geomTransf = geomTransf
        

    @abstractmethod
    def initialize(self):
        ...
    
    @ abstractmethod
    def getNodalDisp(self) -> ndarray:
        ...

    @abstractmethod
    def setElementDeformations(self):
        ...

    @abstractmethod
    def elementStateDetermination(self):
        ...
    
    @abstractmethod
    def getElementForces(self) -> ndarray:
        ...
    
    @abstractmethod
    def getElementStiffness(self) -> ndarray:
        ...
    
    @abstractmethod
    def getDofIDs(self):
        return self.nodeI.getDofIDs() + self.nodeJ.getDofIDs()