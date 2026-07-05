from .section import Section
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
        self.sectionDeformations = np.zeros((2,1))
        '''
        An elastic section does not contain materials with internal state.
        Therefore, it is necessary to store at least the section deformations
        in order to compute the section forces.
        '''

    # -----------------------------------------------------
    #       SECTION STATE DETERMINATION - start
    # -----------------------------------------------------
    def setSectionDeformations(self, e: ndarray) -> None:
        '''
        e: section deformations {eps, curvature}^t
        '''
        self.sectionDeformations = e


    def getSectionForces(self) -> ndarray:
        e = self.sectionDeformations
        k = self.getSectionStiffness()
        ''' s: section forces '''
        s = k @ e
        return s 

    def getSectionStiffness(self) -> ndarray:
        EA,EI = self.E*self.A , self.E*self.I
        ''' k: section stiffness '''
        k = np.array([
            [EA,0],
            [0,EI]
            ],dtype=float)
        return k
    
    # -----------------------------------------------------
    #       SECTION STATE DETERMINATION - end
    # -----------------------------------------------------

    def getCopy(self):
        return ElasticSection(
            id=self.id,
            E=self.E,
            A=self.A,
            I=self.I
        )