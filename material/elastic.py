from __future__ import annotations
from .material import Material, MaterialState


class Elastic(Material):
    '''
	linear elastic material (E constant)
	'''
    def __init__(
            self,
            id: int | str,
            E: float,
            rho: float = 0.0
    ) -> None:
        super().__init__(id=id, rho=rho)
        if E <= 0:
            raise ValueError(f"Material {id}: attribute E must be positive")
        self.E = E
        self.state = MaterialState()
        

    def compute(
		    self,
		    eps: float,
	) -> tuple[float, float]:
        sig = self.E * eps
		# update trial state
        # caller (Solver) will call commit()
        self.state.epsTrial = eps
        self.state.sigTrial = sig
        return sig, self.E
    
    def getCopy(self):
        return Elastic(
            id = self.id,
            E = self.E,
            rho = self.rho
        )

    def toDict(self) -> dict:
        return {
			"type": "elastic",
			"id": self.id,
			"E": self.E,
			"rho": self.rho,
		}

    @classmethod
    def fromDict(cls, data: dict) -> Material:
        return cls(
			id=data["id"],
			rho=data.get("rho", 0.0),
			E=data.get("E", 0.0)
		)