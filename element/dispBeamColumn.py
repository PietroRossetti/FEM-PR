from element.element import Element
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

        self.initialize()
    
    def initialize(self):
        
        theSection = self.beamIntegration.getTheSection()
        nIP = self.beamIntegration.nIP
        self.sections = [theSection.getCopy() for _ in range(nIP)]
        
        self.initialLength = self.geomTransf.getLength()

    
    def getDofIDs(self):
        return super().getDofIDs()
    
    def getNodalDisp(self) -> ndarray:
        '''
        assemble element displacements for node I,J displacements
        '''
        U = np.zeros((6,1))
        dispNodeI = self.nodeI.getDisp()
        dispNodeJ = self.nodeJ.getDisp()

        U[0:3, 0:1] = dispNodeI
        U[3:6, 0:1] = dispNodeJ
        return U
    
    def setElementDeformations(self):
        L = self.initialLength
        # U: nodal displacements in global coords
        U = self.getNodalDisp()
        # T: geometric transformation matrix
        T = self.geomTransf.getTransfMatrix()
        # u: nodal displacements in local coordinates
        u = T @ U
        # num of gauss IP, locations and weights
        nIP = self.beamIntegration.nIP
        Xi = self.beamIntegration.getLocations(L)

        for i in range(nIP):
            x = Xi[i]
            # B: derivative matrix of disp shape function
            B = self.getBmatrix(x, L)
            # e: section deformations at currrent control section (gauss IP)
            e = B @ u
            self.sections[i].setSectionDeformations(e)


    def elementStateDetermination(self):
        L = self.initialLength
        # num of gauss IP, locations and weights
        nIP = self.beamIntegration.nIP
        Xi = self.beamIntegration.getLocations(L)
        Wt = self.beamIntegration.getWeights(L)
        # F, K: element forces and element stiffness
        F = np.zeros((6,1))
        K = np.zeros((6,6))

        for i in range(nIP):
            x = Xi[i]
            wt = Wt[i]

            # B: derivative matrix of disp shape function
            B = self.getBmatrix(x, L)
            # s, k: section forces and section stiffness at current control section
            s = self.sections[i].getSectionForces()
            k = self.sections[i].getSectionStiffness()

            F += (B.T @ s)*wt
            K += (B.T @ k @ B)*wt

        return F,K


    def getElementForces(self):
        F, _ = self.elementStateDetermination()
        T = self.geomTransf.getTransfMatrix()
        Fg = T.T @ F # element forces in global coords
        return Fg


    def getElementStiffness(self):
        _, K = self.elementStateDetermination()
        T = self.geomTransf.getTransfMatrix()
        Kg = T.T @ K @ T # element stiffness in global coords
        return Kg
    

    @staticmethod
    def getBmatrix(x:float, L:float) -> ndarray:
        ''' derivative of displacement shape function for displacement-based beam-column element '''
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