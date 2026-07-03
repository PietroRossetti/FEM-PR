from .section import Section, SectionState
from material.material import Material
from numpy import ndarray
import numpy as np



class Aggregator(Section):
    def __init__(
            self,
            id: int | str,
            axialMaterial: Material,
            bendingMaterial: Material
    ):
        super().__init__(id)

        self.axialMaterial = axialMaterial
        self.bendingMaterial = bendingMaterial
        self.sectionState = SectionState()
        self.sectionStiffness = np.zeros((2,2))

    def setTrialSectionDeformation(self, deformations: ndarray) -> None:
        
        self.sectionState.sectionDeformationsTrial = deformations
        N, EA = self.axialMaterial.compute(float(deformations[0, 0]))
        M, EI = self.bendingMaterial.compute(float(deformations[1, 0]))

        s = np.array([
            [N],
            [M]
        ])
        k = np.array([
            [EA, 0.0],
            [0.0, EI]
        ])
        
        self.sectionState.sectionForcesTrial = s
        self.sectionStiffness = k

    def getSectionForces(self) -> ndarray:
        return self.sectionState.sectionForcesTrial

    def getSectionStiffness(self) -> ndarray:
        return self.sectionStiffness

    def getCopy(self):
        return Aggregator(
            id= self.id,
            axialMaterial = self.axialMaterial.getCopy(),
            bendingMaterial = self.bendingMaterial.getCopy()
        )