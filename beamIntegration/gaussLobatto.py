from __future__ import annotations

from section.section import Section

from .beamIntegration import BeamIntegration


class GaussLobatto(BeamIntegration):
    integrationType = "lobatto"

    def _get_rule(self, nIP: int) -> tuple[list[float], list[float]]:
        match nIP:
            case 1:
                raise ValueError("GaussLobatto requires at least 2 integration points")
            case 2:
                return [-1.0, 1.0], [1.0, 1.0]
            case 3:
                return [-1.0, 0.0, 1.0], [1 / 3, 4 / 3, 1 / 3]
            case 4:
                return (
                    [-1.0, -0.4472135954999579, 0.4472135954999579, 1.0],
                    [1 / 6, 5 / 6, 5 / 6, 1 / 6] )
            
            case 5:
                return (
                    [-1.0, -0.6546536707079772, 0.0, 0.6546536707079772, 1.0],
                    [0.1, 0.5444444444444444, 0.7111111111111111, 0.5444444444444444, 0.1] )
            
            case 6:
                return (
                    [-1.0, -0.7650553239294647, -0.2852315164806451, 0.2852315164806451, 0.7650553239294647, 1.0],
                    [0.0666666666666667, 0.3784749562978470, 0.5548583770354863, 0.5548583770354863, 0.3784749562978470, 0.0666666666666667] )
            
            case 7:
                return (
                    [-1.0, -0.8302238962785669, -0.4688487934707142, 0.0, 0.4688487934707142, 0.8302238962785669, 1.0],
                    [0.0476190476190476, 0.276826047361566, 0.4317453812098627, 0.4876190476190476, 0.4317453812098627, 0.276826047361566, 0.0476190476190476] )
            
            case 8:
                return (
                    [-1.0, -0.8717401485096066, -0.5917001814331423, -0.2092992179024789, 0.2092992179024789, 0.5917001814331423, 0.8717401485096066, 1.0],
                    [0.0357142857142857, 0.2107042271435061, 0.3411226924835044, 0.4124587946587038, 0.4124587946587038, 0.3411226924835044, 0.2107042271435061, 0.0357142857142857] )
            
            case _:
                raise ValueError("GaussLobatto supports 2 to 8 integration points")

    def getCopy(self) -> BeamIntegration:
        return GaussLobatto(
            id=self.id,
            nIP=self.nIP,
            section=self.theSection
        )
