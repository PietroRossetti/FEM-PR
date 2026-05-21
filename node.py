from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Node:
    id: int | str
    x: float
    y: float
    z: float = 0.0
    
    DOFs: list = field(default_factory=list)
    '''
    displacements: dict = field(default_factory=dict)
    reactions: dict = field(default_factory=dict)
    constraints: dict = field(default_factory=dict)
    '''
    def getCoord(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "DOFs": self.DOFs            
        }
    
    @classmethod
    def fromDict(cls, data: dict)->Node:
        return cls(
            id = data["id"],
            x  = data["x"],
            y  = data["y"],
            z  = data["z"],
            DOFs = data.get("DOFs",[])
        )
