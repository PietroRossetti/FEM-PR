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
        

    def compute(
		    self,
		    eps: float,
		    state: MaterialState
	) -> tuple[float, float]:
        sig = self.E * eps
		# update trial state
        # caller (Solver) will call commit()
        state.epsTrial = eps
        state.sigTrial = sig
        return sig, self.E

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