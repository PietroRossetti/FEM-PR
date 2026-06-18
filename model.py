from __future__ import annotations
from typing import TYPE_CHECKING

from domain import Domain

# material types
from material.elastic import Elastic
from material.steel01 import Steel01
# section types
from section.section import Section
from section.aggregator import Aggregator
from section.elasticSection import ElasticSection

# beam integration types
from beamIntegration.gaussLegendre import GaussLegendre
from beamIntegration.gaussLobatto import GaussLobatto


class Model(Domain):
    '''
    create a database for each type in the framework
    '''
    def __init__(self) -> None:
        super().__init__()

    # ----------------------------------------------------------------------------------------------
    #           IMPORT TYPES (material, section, beamIntegration)
    # ----------------------------------------------------------------------------------------------
    def material(self, materialType: str, *args, **kwargs):
        if materialType == "elastic":
            return self.addElasticMaterial(*args, **kwargs)
        if materialType == "steel01":
            return self.addSteel01Material(*args, **kwargs)

        raise ValueError(f"Unknown material type {materialType!r}")

    def section(self, sectionType: str, *args, **kwargs):
        if sectionType == "elasticSection":
            return self.addElasticSection(*args, **kwargs)
        if sectionType == "aggregator":
            return self.addAggregator(*args, **kwargs)

        raise ValueError(f"Unknown section type {sectionType!r}")
    
    def beamIntegration(self, integrationType: str, *args, **kwargs):
        if integrationType == "lobatto":
            return self.addGaussLobatto(*args, **kwargs)
        if integrationType == "legendre":
            return self.addGaussLegendre(*args, **kwargs)
        
        raise ValueError(f"Unknown integration type {integrationType!r}")

    def element(self, elementType: str, *args, **kwargs):
        raise ValueError(f"Unknown element type {elementType!r}")
    


    # ----------------------------------------------------------------------------------------------
    #           MATERIAL LIBRARY
    # ----------------------------------------------------------------------------------------------

    def addElasticMaterial(self, id: int | str, E: float, rho: float = 0.0) -> Elastic:

        material = Elastic(id=id, E=E, rho=rho)
        self.addMaterial(material)

        return material

    def addSteel01Material(self, id: int | str, fy: float, E0: float, b: float, a1: float = 0.07, a2: float = 2, a3: float = 0.07, a4: float = 2, rho: float = 0.0) -> Steel01:

        material = Steel01(id=id, fy=fy, E0=E0, b=b, a1=a1, a2=a2, a3=a3, a4=a4, rho=rho)
        self.addMaterial(material)

        return material
    
    # ----------------------------------------------------------------------------------------------
    #           SECTION LIBRARY
    # ----------------------------------------------------------------------------------------------

    def addElasticSection(self, id: int | str, E: float, A: float, I: float) -> ElasticSection:

        section = ElasticSection(id=id, E=E, A=A, I=I)
        self.addSection(section)

        return section

    def addAggregator(self, id: int | str, axialID: int | str, bendingID: int | str) -> Aggregator:

        section = Aggregator(
            id=id,
            axialMaterial=self.getMaterialCopy(axialID),
            bendingMaterial=self.getMaterialCopy(bendingID)
        )
        self.addSection(section)

        return section


    # ----------------------------------------------------------------------------------------------
    #           BEAM INTEGRATION LIBRARY
    # ----------------------------------------------------------------------------------------------

    def addGaussLegendre(self, id: int | str, nIP: int, sectionID: int | str) -> GaussLegendre:

        beamIntegration = GaussLegendre(
            id=id,
            nIP=nIP,
            section=self.getSection(sectionID)
        )
        self.addBeamIntegration(beamIntegration)

        return beamIntegration
    
    def addGaussLobatto(self, id: int | str, nIP: int, sectionID: int | str) -> GaussLobatto:

        beamIntegration = GaussLobatto(
            id=id,
            nIP=nIP,
            section=self.getSection(sectionID)
        )
        self.addBeamIntegration(beamIntegration)

        return beamIntegration
