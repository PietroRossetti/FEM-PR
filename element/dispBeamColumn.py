from element.element import Element, ElementState

from node import Node
from beamIntegration.beamIntegration import BeamIntegration
from geometricTransformation.geometricTransformation import GeometricTransformation

import numpy as np
from numpy import ndarray

class DispBeamColumn(Element):
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
        self.sections = []
        self.geomTransf = geomTransf
        self.eleState = ElementState()

        self.initialize()
    
    def initialize(self):
        
        theSection = self.beamIntegration.getTheSection()
        nIP = self.beamIntegration.nIP
        self.sections = [theSection.getCopy() for _ in range(nIP)]
        
        self.initialLength = self.geomTransf.getLength()
        
        self.eleState.eleDispCommitted = np.zeros((6,1))
        self.eleState.eleDispTrial = np.zeros((6,1))
        self.eleState.eleForcesCommitted = np.zeros((6,1))
        self.eleState.eleForcesTrial = np.zeros((6,1))
        
        self.eleStiffness = np.zeros((6,6))

    
    def getDofIDs(self):
        return super().getDofIDs()
    
    def setTrialDisp(self, displacements: ndarray):

        # U: nodal displacements in global coordinates
        U = displacements
        # T: geometric transformation matrix
        T = self.geomTransf.getTransfMatrix()
        # u: nodal displacements in local coordinates
        u = T @ U
        # num of gauss IP, locations and weights
        nIP = self.beamIntegration.nIP
        Xi = self.beamIntegration.getLocations(self.initialLength)
        Wt = self.beamIntegration.getWeights(self.initialLength)
        # F, K: element forces and element stiffness
        F = np.zeros((6,1))
        K = np.zeros((6,6))
        for i in range(nIP):
            x = Xi[i]
            wt = Wt[i]
            L = self.initialLength
            # B: derivative matrix of disp shape function
            B = self.getBmatrix(x, L)
            # e: section deformations at currrent control section (gauss IP)
            e = B @ u
            self.sections[i].setTrialSectionDeformation(e)

            # s, k: section forces and section stiffness at current control section
            s = self.sections[i].getSectionForces()
            k = self.sections[i].getSectionStiffness()

            F += (B.T @ s)*wt
            K += (B.T @ k @ B)*wt

        self.eleState.eleDispTrial = U
        self.eleState.eleForcesTrial = (T.T @ F)
        self.eleStiffness = (T.T @ K @ T)


    def getEleForces(self):
        return self.eleState.eleForcesTrial
    
    def getEleStiffness(self):
        return self.eleStiffness
    

    @staticmethod
    def getBmatrix(x:float, L:float) -> ndarray:

        # bending shape functions
        B1 = -6/L**2 + x*12/L**3
        B2 = x*6/L**2 - 4/L
        B3 = 6/L**2 - x*12/L**3
        B4 = -2/L + x*6/L**2
        # axial shape functions
        B5 = -1/L
        B6 = 1/L

        B = np.array([
            [B5,0,0,B6,0,0],
            [0,B1,B2,0,B3,B4]
        ])

        return B
