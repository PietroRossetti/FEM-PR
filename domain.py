from __future__ import annotations

from node import Node
from material.material import Material
from section.section import Section


class Domain:
    """
    Repository of model objects.

    Materials and sections stored here are prototypes. Components that need a
    stateful instance should ask for a copy, so the prototype state stays clean.
    """

    def __init__(self) -> None:
        self.nodes: dict[int | str, Node] = {}
        self.materials: dict[int | str, Material] = {}
        self.sections: dict[int | str, Section] = {}
        self.elements: dict[int | str, object] = {}

    def addNode(self, node: Node) -> None:
        self._add(self.nodes, node, "node")

    def addMaterial(self, material: Material) -> None:
        self._add(self.materials, material, "material")

    def addSection(self, section: Section) -> None:
        self._add(self.sections, section, "section")

    def addElement(self, element) -> None:
        self._add(self.elements, element, "element")

    def getNode(self, id: int | str) -> Node:
        return self._get(self.nodes, id, "node")

    def getMaterial(self, id: int | str) -> Material:
        return self._get(self.materials, id, "material")

    def getSection(self, id: int | str) -> Section:
        return self._get(self.sections, id, "section")

    def getElement(self, id: int | str):
        return self._get(self.elements, id, "element")

    def getMaterialCopy(self, id: int | str) -> Material:
        return self._get_copy(self.materials, id, "material")

    def getSectionCopy(self, id: int | str) -> Section:
        return self._get_copy(self.sections, id, "section")

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
