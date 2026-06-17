from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class MaterialState:
    '''
    state of a material (to date, only uniaxial materials)
    - commit state: equilibrium state at the previous step
    - trial state: material state at the current iteration

    modified by Solver
    '''

    epsCommitted: float = 0.0 # converged strain
    sigCommitted: float = 0.0 # converged stress
    hstvCommitted: dict = field(default_factory=dict) # converged history variables

    epsTrial: float = 0.0 # trial strain
    sigTrial: float = 0.0 # trial stress
    hstvTrial: dict = field(default_factory=dict) # trial history variables

    def commit(self) -> None:
        '''Solver transfer trial state to committed state after converged iteration'''
        self.epsCommitted = self.epsTrial
        self.sigCommitted = self.sigTrial
        self.hstvCommitted = self.hstvTrial.copy()

    def revert(self) -> None:
        '''Solver revert to committed after diverged iteration (e.g. for adaptive time step)'''
        self.epsTrial = self.epsCommitted
        self.sigTrial = self.sigCommitted
        self.hstvTrial = self.hstvCommitted.copy()

    
    def toDict(self) -> dict:
        '''create dict from MaterialState instance'''
        return {
            "epsCommitted": self.epsCommitted,
            "sigCommitted": self.sigCommitted,
            "hstvCommitted": self.hstvCommitted,
            "epsTrial": self.epsTrial,
            "sigTrial": self.sigTrial,
            "hstvTrial": self.hstvTrial
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
    def compute(
        self,
        eps: float,
    ) -> tuple[float, float]:
        '''
        compute stress and stiffness given strain

        I: eps (trial strain epsP + deps)
           state (committed material state) 
        O:  sig (trial stress)
            E   (trial stiffness)
        '''
        ...

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