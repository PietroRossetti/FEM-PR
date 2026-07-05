from .section import Section
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

    def setSectionDeformations(self, e: ndarray) -> None:
        '''
        e: section deformations {eps, curvature}^t
        '''
        self.axialMaterial.compute(float(e[0, 0]))
        self.bendingMaterial.compute(float(e[1, 0]))


    def getSectionForces(self) -> ndarray:
        N = self.axialMaterial.getStress()
        M = self.bendingMaterial.getStress()
        ''' s: section forces '''
        s = np.array([
            [N],
            [M]
        ])
        return s

    def getSectionStiffness(self) -> ndarray:
        EA = self.axialMaterial.getTangent()
        EI = self.bendingMaterial.getTangent()
        ''' k: section stiffness '''
        k = np.array([
            [EA, 0.0],
            [0.0, EI]
        ])
        return k

    def getCopy(self):
        return Aggregator(
            id= self.id,
            axialMaterial = self.axialMaterial.getCopy(),
            bendingMaterial = self.bendingMaterial.getCopy()
        )