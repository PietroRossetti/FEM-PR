from numpy import ndarray
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from node import Node
from section.section import Section

class GeometricTransformation():
    ...


class ElementState:

    eleDeformationsCommitted: ndarray
    eleForcesCommitted: ndarray

    eleDeformationsTrial: ndarray
    eleForcesTrial: ndarray

    def commit(self):
        self.eleDeformationsCommitted = self.eleDeformationsTrial
        self.elementForcesCommitted = self.eleForcesCommitted
    
    def revert(self):
        self.eleDeformationsTrial = self.eleDeformationsCommitted
        self.eleForcesTrial = self.eleForcesCommitted


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
        self.s