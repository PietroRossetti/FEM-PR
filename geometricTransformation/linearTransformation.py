from geometricTransformation.geometricTransformation import GeometricTransformation
from node import Node
from math import sqrt
import numpy as np

class LinearTransformation(GeometricTransformation):
    def __init__(self, id: int|str, nodeI: Node | None = None, nodeJ: Node | None = None):
        super().__init__(id, nodeI, nodeJ)

        self.L = None
        self.c = None
        self.s = None

        if nodeI is not None and nodeJ is not None:
            self.initialize()

    def initialize(self):
        xA, yA = self.nodeI.getCoord()
        xB, yB = self.nodeJ.getCoord()

        dx = xB - xA
        dy = yB - yA
        L = sqrt(dx**2 + dy**2)

        if L == 0:
            raise ValueError("Geometric transformation has zero length.")

        c = dx / L
        s = dy / L

        self.L = L
        self.c = c
        self.s = s



    def update(self):
        ''' Linear transformation parameters are constant during the analysis '''
        ...

    def getLength(self):
        return self.L

    def getTransfMatrix(self):
        c = self.c
        s = self.s

        t = np.array([
            [ c,  s, 0],
            [-s,  c, 0],
            [ 0,  0, 1]
        ],dtype=float)

        T = np.zeros((6, 6))
        T[0:3, 0:3] = t
        T[3:6, 3:6] = t 
        return T
    
    def getCopy(self, nodeI, nodeJ) -> LinearTransformation:
        return LinearTransformation(
            id = self.id,
            nodeI = nodeI,
            nodeJ = nodeJ
        )