from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Node:
    id: int | str
    x: float
    y: float
    
    DOFs: list = field(default_factory=list)
    '''
    displacements: dict = field(default_factory=dict)
    reactions: dict = field(default_factory=dict)
    constraints: dict = field(default_factory=dict)
    '''
    def getCoord(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def getDofIDs(self) -> list:
        return self.DOFs

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "DOFs": self.DOFs            
        }
    
    @classmethod
    def fromDict(cls, data: dict)->Node:
        return cls(
            id = data["id"],
            x  = data["x"],
            y  = data["y"],
            DOFs = data.get("DOFs",[])
        )
