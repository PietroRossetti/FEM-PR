from __future__ import annotations
from node import Node
from abc import ABC, abstractmethod


class GeometricTransformation(ABC):
    def __init__(self, id: int|str, nodeI: Node | None = None, nodeJ: Node | None = None):
        self.id = id
        self.nodeI = nodeI
        self.nodeJ = nodeJ

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def getLength(self):
        ...

    @abstractmethod
    def getTransfMatrix(self):
        ...

    @abstractmethod
    def getCopy(self, nodeI: Node, nodeJ: Node):
        ...