from domain import Domain
from material.elastic import Elastic
from material.steel01 import Steel01
from section.aggregator import Aggregator
from section.elasticSection import ElasticSection



class Model(Domain):
    '''
    create a database for each type in the framework
    '''
    def __init__(self) -> None:
        super().__init__()

    def material(self, materialType: str, **kwargs):
        materialType = self._normalize_type(materialType)

        if materialType == "elastic":
            return self.addElasticMaterial(**kwargs)
        if materialType == "steel01":
            return self.addSteel01Material(**kwargs)

        raise ValueError(f"Unknown material type {materialType!r}")

    def section(self, sectionType: str, **kwargs):
        sectionType = self._normalize_type(sectionType)

        if sectionType in ("elastic", "elasticsection"):
            return self.addElasticSection(**kwargs)
        if sectionType == "aggregator":
            return self.addAggregator(**kwargs)

        raise ValueError(f"Unknown section type {sectionType!r}")

    def element(self, elementType: str, **kwargs):
        elementType = self._normalize_type(elementType)
        raise ValueError(f"Unknown element type {elementType!r}")

    def addElasticMaterial(
            self,
            id: int | str,
            E: float,
            rho: float = 0.0
    ) -> Elastic:
        material = Elastic(id=id, E=E, rho=rho)
        self.addMaterial(material)
        return material

    def addSteel01Material(
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
    ) -> Steel01:
        material = Steel01(
            id=id,
            fy=fy,
            E0=E0,
            b=b,
            a1=a1,
            a2=a2,
            a3=a3,
            a4=a4,
            rho=rho
        )
        self.addMaterial(material)
        return material

    def addElasticSection(
            self,
            id: int | str,
            E: float,
            A: float,
            I: float
    ) -> ElasticSection:
        section = ElasticSection(id=id, E=E, A=A, I=I)
        self.addSection(section)
        return section

    def addAggregator(
            self,
            id: int | str,
            axialID: int | str,
            bendingID: int | str
    ) -> Aggregator:
        section = Aggregator(
            id=id,
            axialMaterial=self.getMaterialCopy(axialID),
            bendingMaterial=self.getMaterialCopy(bendingID)
        )
        self.addSection(section)
        return section

    def _normalize_type(self, objectType: str) -> str:
        return objectType.lower().replace("_", "").replace("-", "")
