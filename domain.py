from __future__ import annotations

from node import Node
from material.material import Material
from section.section import Section
from beamIntegration.beamIntegration import BeamIntegration
from geometricTransformation.geometricTransformation import GeometricTransformation
from element.element import Element


class Domain:
    """
    Repository of model objects.

    Materials and sections defined by user are stored here.
    Instance that requires a copy (es. uniaxial material) remain untouched
    """

    def __init__(self) -> None:
        self.nodes: dict[int | str, Node] = {}
        self.materials: dict[int | str, Material] = {}
        self.sections: dict[int | str, Section] = {}
        self.beamIntegrations: dict[int | str, BeamIntegration] = {}
        self.geometricTransformations: dict[int|str, GeometricTransformation] = {}
        self.elements: dict[int | str, Element] = {}

    def addNode(self, node: Node) -> None:
        self._add(self.nodes, node, "node")

    def addMaterial(self, material: Material) -> None:
        self._add(self.materials, material, "material")

    def addSection(self, section: Section) -> None:
        self._add(self.sections, section, "section")

    def addBeamIntegration(self, beamIntegration: BeamIntegration) -> None:
        self._add(self.beamIntegrations, beamIntegration, "beamIntegration")
    
    def addGeometricTransformation(self, geomTransf: GeometricTransformation) -> None:
        self._add(self.geometricTransformations, geomTransf, "geometricTransformation")

    def addElement(self, element) -> None:
        self._add(self.elements, element, "element")



    def getNode(self, id: int | str) -> Node:
        return self._get(self.nodes, id, "node")

    def getMaterial(self, id: int | str) -> Material:
        return self._get(self.materials, id, "material")

    def getSection(self, id: int | str) -> Section:
        return self._get(self.sections, id, "section")
    
    def getBeamIntegration(self, id: int|str) -> BeamIntegration:
        return self._get(self.beamIntegrations, id, "beamIntegration")
    
    def getGeomTransf(self, id: int|str) -> GeometricTransformation:
        return self._get(self.geometricTransformations, id, "geometricTransformation")

    def getElement(self, id: int | str) -> Element:
        return self._get(self.elements, id, "element")
    


    def getMaterialCopy(self, id: int | str) -> Material:
        return self._get_copy(self.materials, id, "material")

    def getSectionCopy(self, id: int | str) -> Section:
        return self._get_copy(self.sections, id, "section")
    
    def getBeamIntegrationCopy(self, id: int|str) -> BeamIntegration:
        return self._get_copy(self.beamIntegrations, id, "beamIntegration")
    
    def getGeomTransfCopy(self, id: int|str, nodeI: Node, nodeJ: Node) -> GeometricTransformation:

        geoTransf = self.getGeomTransf(id)

        try:
            return geoTransf.getCopy(nodeI, nodeJ)
        except AttributeError as exc:
            raise TypeError(f"GEOMETRIC TRANSFORMATION {id!r} does not implement getCopy()") from exc
    
    

    def _add(self, objects: dict, obj, objectType: str) -> None:
        if obj.id in objects:
            raise ValueError(f"Domain already contains {objectType} with id {obj.id!r}")
        objects[obj.id] = obj

    def _get(self, objects: dict, id: int | str, objectType: str):
        try:
            return objects[id]
        except KeyError as exc:
            raise KeyError(f"Domain does not contain {objectType} with id {id!r}") from exc

    def _get_copy(self, objects: dict, id: int | str, objectType: str):
        obj = self._get(objects, id, objectType)
        try:
            return obj.getCopy()
        except AttributeError as exc:
            raise TypeError(f"{objectType.capitalize()} {id!r} does not implement getCopy()") from exc