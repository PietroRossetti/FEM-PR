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

        e = deformations
        EA,EI = self.E*self.A , self.E*self.I
        k = np.array([
            [EA,0.],
            [0.,EI]
        ])
        s = k @ e

        self.sectionState.sectionForcesTrial = s
        self.sectionStiffness = k


    def getSectionForces(self) -> ndarray:
        return self.sectionState.sectionForcesTrial

    def getSectionStiffness(self) -> ndarray:
        return self.sectionStiffness

    def getCopy(self):
        return ElasticSection(
            id=self.id,
            E=self.E,
            A=self.A,
            I=self.I
        )