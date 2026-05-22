from __future__ import annotations
from .material import Material, MaterialState

'''
bilinear material with isotropic hardening
'''
class Steel01(Material):
    def __init__(
            self,
            id: int | str,
            fy: float,
            E0: float,
            b: float,
            a1: float = 0.07,
            a2: float = 2,
            a3: float = 0.07,
            a4: float = 2,
            rho: float = 0.0
    ) -> None:
        super().__init__(id=id, rho=rho)
        self.fy = fy
        self.E0 = E0
        self.b = b
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        # --------------------------------------------------
        # calculate fixed material properties
        # --------------------------------------------------
        self.Eh = self.b * self.E0
        self.epsy = self.fy/self.E0

    def compute(
            self,
            eps: float,
            state: MaterialState
    ) -> tuple[float,float]:
        
        # --------------------------------------------------
        # retrieve history variables
        # --------------------------------------------------
        epsP = state.epsCommitted                       # strain at previous converged step
        sigP = state.sigCommitted                       # stress at previous converged step
        epsmin = state.hstvCommitted.get("epsmin",0.0)  # max eps in compression
        epsmax = state.hstvCommitted.get("epsmax",0.0)  # max eps in tension
        # --------------------------------------------------
        # calculate current strain increment
        # -------------------------------------------------- 
        deps = eps - epsP   
        # --------------------------------------------------
        # isotropic hardening
        # --------------------------------------------------
        hc = max(
            self.fy * self.a1 * (epsmax/self.epsy - self.a2),
            0.0 )
        ht = max(
            self.fy * self.a3 * (abs(epsmin/self.epsy) - self.a4),
            0.0 )
        # --------------------------------------------------
        # bilinear model
        # --------------------------------------------------
        c1 = self.Eh * eps
        c2 = (self.fy + hc)*(1 - self.b)
        c3 = (self.fy + ht)*(1 - self.b)

        c = sigP + self.E0*deps

        sig = max(
            c1 - c2,
            min( (c1+c3), c) )
        
        Et = self.Eh
        if abs(sig-c) < 1e-10:
            Et = self.E0
        # --------------------------------------------------
        # update history variables
        # --------------------------------------------------
        epsmin = min(eps, epsmin)
        epsmax = max(eps, epsmax)
        # --------------------------------------------------
        # update trial state
        # --------------------------------------------------
        state.epsTrial = eps
        state.sigTrial = sig
        state.hstvTrial = {
            "epsmin": epsmin,
            "epsmax": epsmax }
        
        return sig, Et
    

    def toDict(self) -> dict:
        return {
            "type": "steel01",
            "id": self.id,
            "fy": self.fy,
            "E0": self.E0,
            "b": self.b,
            "a1": self.a1,
            "a2": self.a2,
            "a3": self.a3,
            "a4": self.a4,
            "rho": self.rho
        }
    
    @classmethod
    def fromDict(cls, data:dict) -> Steel01:
        return cls(
            id=data["id"],
            fy=data["fy"],
            E0=data["E0"],
            b=data["b"],
            a1=data.get("a1", 0.07),
            a2=data.get("a2", 2.0),
            a3=data.get("a3", 0.07),
            a4=data.get("a4", 2.0),
            rho=data.get("rho", 0.0)
        )
    
    def __repr__(self) -> str:
        return f"steel01 (id={self.id!r}, fy={self.fy}, E0={self.E0}, b={self.b}, a1={self.a1}, a2={self.a2}, a3={self.a3}, a4={self.a4})"