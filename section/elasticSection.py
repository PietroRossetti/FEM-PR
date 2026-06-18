from section import Section
from numpy import ndarray
import numpy as np

class ElasticSection(Section):
    def __init__(
            self,
            id: int | str,
            E: float,
            A: float,
            I: float

    ):
        super().__init__(id)
        self.E = E
        self.A = A
        self.I = I

    def setTrialSectionDeformation(self, deformations: ndarray) -> None:
        self.sectionState.sectionDeformationsTrial = deformations
    
    def getSectionForces(self):
        e = self.sectionState.sectionDeformationsTrial
        k = self.getSectionStiffness()
        s = k @ e
        return s

    def getSectionStiffness(self):
        EA = self.E * self.A
        EI = self.E* self.I
        k = np.array([
            [EA, 0.0],
            [0.0, EI]
        ])
        return k

    def getCopy(self):
        return ElasticSection(
            id=self.id,
            E=self.E,
            A=self.A,
            I=self.I
        )
