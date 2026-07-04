from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class MaterialState:
    '''
    state of a material (to date, only uniaxial materials)
    - commit state: equilibrium state at the previous step (suffix P)
    - trial state: material state at the current iteration (same quantities as above without suffix P)

    modified by Solver
    '''

    strainP:  float = 0.0  # converged strain
    stressP:  float = 0.0  # converged stress
    tangentP: float = 0.0 # converged tangent stiffness
    hstvP:    dict  = field(default_factory=dict) # converged history variables

    strain:  float = 0.0 # trial strain
    stress:  float = 0.0 # trial stress
    tangent: float = 0.0 # trial tangent stiffness
    hstv:    dict  = field(default_factory=dict) # trial history variables

    def commit(self) -> None:
        '''Solver transfer trial state to committed state after converged iteration'''
        self.strainP = self.strain
        self.stressP = self.stress
        self.tangentP = self.tangent
        self.hstvP = self.hstv.copy()

    def revert(self) -> None:
        '''Solver revert to committed after diverged iteration (e.g. for adaptive time step)'''
        self.strain = self.strainP
        self.stress = self.stressP
        self.tangent = self.tangentP
        self.hstv = self.hstvP.copy()

    
    def toDict(self) -> dict:
        '''create dict from MaterialState instance'''
        return {
            "strainP": self.strainP,
            "stressP": self.stressP,
            "tangentP": self.tangentP,
            "hstvP": self.hstvP,
            "strain": self.strain,
            "stress": self.stress,
            "tangent": self.tangent,
            "hstv": self.hstv
        }
    
    @classmethod
    def fromDict(cls, data: dict) -> MaterialState:
        '''create MaterialState instance from dict'''
        return cls(**data)


class Material(ABC):
    '''
    abstract class for all material
    - compute(eps) -> sig, E
    - toDict, fromDict
    '''
    def __init__(
            self,
            id: int | str,
            rho: float = 0.0
    ) -> None:
        
        self.id = id
        self.rho = rho
        self.state = MaterialState()
    

    @abstractmethod
    def compute(self, eps: float) -> tuple[float, float]:
        '''
        compute stress and stiffness given strain and update trial state

        I: eps (trial strain epsP + deps)
        O: sig (trial stress)
           E   (trial tangent stiffness)
        '''
        ...
    
    @abstractmethod
    def getStress(self) -> float:
        return self.state.stress
    
    @abstractmethod
    def getTangent(self) -> float:
        return self.state.tangent

    @abstractmethod
    def getCopy(self):
        # return a copy (es. return Elastic(id = self.id, E = self.E, rho = self.rho) )
        ...
    
    @abstractmethod
    def toDict(self) -> dict:
        '''
        create dict from Material instance
        '''
        ...

    @classmethod
    @abstractmethod
    def fromDict(cls, data: dict) -> Material:
        '''
        create Material instance from dict
        '''
        ...
    
    def materialTester(
            self,
            strainHistory: list[float],
    ) -> tuple[ list[float], list[float] ]:
        '''
        material tester for new implementation
        Given strain history return stress and stiffness history using material routine
        each step of strain history is committed
        '''

        stressHistory, stiffnessHistory = [] , []

        for strain in strainHistory:

            stress, stiffness = self.compute(strain)
            self.state.commit()
            stressHistory.append(stress)
            stiffnessHistory.append(stiffness)

        return stressHistory, stiffnessHistory
    

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"