from __future__ import annotations
from dataclasses import dataclass, field
from numpy import array, ndarray, zeros

@dataclass
class NodeState:
    '''
    - commit state: equilibrium state at the previous step (suffix P)
    - trial state: node state at the current iteration (same quantities as above without suffix P)

    modified by Solver
    '''
    dispP: ndarray = field(default_factory= lambda: zeros((3,1))) # converged nodal displacements
    velP:  ndarray = field(default_factory= lambda: zeros((3,1))) # converged nodal velocities
    accP:  ndarray = field(default_factory= lambda: zeros((3,1))) # converged nodal accelerations

    disp: ndarray = field(default_factory= lambda: zeros((3,1))) # trial nodal displacements
    vel:  ndarray = field(default_factory= lambda: zeros((3,1))) # trial nodal velocities
    acc:  ndarray = field(default_factory= lambda: zeros((3,1))) # trial nodal accelerations

    def commit(self):
        '''Solver transfer trial state to committed state after converged iteration'''
        self.dispP = self.disp.copy()
        self.velP = self.vel.copy()
        self.accP = self.acc.copy()
    
    def revert(self):
        '''Solver revert to committed after diverged iteration (e.g. for adaptive time step)'''
        self.disp = self.dispP.copy()
        self.vel = self.velP.copy()
        self.acc = self.accP.copy()

    def toDict(self) -> dict:
        '''create dict from NodeState instance'''
        return {
            "dispP": self.dispP.tolist(),
            "velP": self.velP.tolist(),
            "accP": self.accP.tolist(),
            "disp": self.disp.tolist(),
            "vel": self.vel.tolist(),
            "acc": self.acc.tolist(),
        }
    
    @classmethod
    def fromDict(cls, data: dict) -> NodeState:
        '''create NodeState instance from dict'''
        return cls(
            dispP=array(data.get("dispP", zeros((3, 1))), dtype=float),
            velP=array(data.get("velP", zeros((3, 1))), dtype=float),
            accP=array(data.get("accP", zeros((3, 1))), dtype=float),
            disp=array(data.get("disp", zeros((3, 1))), dtype=float),
            vel=array(data.get("vel", zeros((3, 1))), dtype=float),
            acc=array(data.get("acc", zeros((3, 1))), dtype=float),
        )


@dataclass
class Node:
    id: int | str
    x: float
    y: float
    
    DOFs: list = field(default_factory=list)
    state: NodeState = field(default_factory=NodeState)
    '''
    STATE (trial and committed state):
    disp = 3x1 vector {Ux, Uy, Rz}^t
    vel, acc...
    '''

    '''
    reactions: dict = field(default_factory=dict)
    constraints: dict = field(default_factory=dict)
    '''
    def getCoord(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def getDofIDs(self) -> list:
        return self.DOFs
    
    def getDisp(self) -> ndarray:
        return self.state.disp

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "DOFs": self.DOFs,
            "state": self.state.toDict(),
        }
    
    @classmethod
    def fromDict(cls, data: dict)->Node:
        return cls(
            id = data["id"],
            x  = data["x"],
            y = data["y"],
            DOFs=data.get("DOFs", []),
            state=NodeState.fromDict(data.get("state", {})),
        )
