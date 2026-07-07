import unittest

import numpy as np

from model import Model


class DispBeamColumnTests(unittest.TestCase):
    def make_vertical_elastic_beam(self):
        model = Model()
        model.node(1, 0.0, 0.0)
        model.node(2, 0.0, 1.0)
        model.section("elasticSection", "sec", 1.0, 10.0, 1.0)
        model.beamIntegration("lobatto", "int", 5, "sec")
        model.geomTransf("linear", "lin")
        beam = model.element("dispBeamColumn", "ele", 1, 2, "lin", "int")
        return model, beam

    def test_elastic_beam_global_stiffness_for_vertical_member(self):
        _, beam = self.make_vertical_elastic_beam()

        np.testing.assert_allclose(
            beam.getElementStiffness(),
            np.array(
                [
                    [12.0, 0.0, -6.0, -12.0, 0.0, -6.0],
                    [0.0, 10.0, 0.0, 0.0, -10.0, 0.0],
                    [-6.0, 0.0, 4.0, 6.0, 0.0, 2.0],
                    [-12.0, 0.0, 6.0, 12.0, 0.0, 6.0],
                    [0.0, -10.0, 0.0, 0.0, 10.0, 0.0],
                    [-6.0, 0.0, 2.0, 6.0, 0.0, 4.0],
                ]
            ),
            atol=1e-12,
        )

    def test_elastic_beam_forces_match_stiffness_times_displacement(self):
        model, beam = self.make_vertical_elastic_beam()
        displacement = np.array([[0.0, 1.0, 0.0, 0.0, 0.0, 0.0]]).T

        model.getNode(1).state.disp = displacement[0:3].copy()
        model.getNode(2).state.disp = displacement[3:6].copy()
        beam.setElementDeformations()

        np.testing.assert_allclose(
            beam.getElementForces(),
            beam.getElementStiffness() @ displacement,
            atol=1e-12,
        )


if __name__ == "__main__":
    unittest.main()
