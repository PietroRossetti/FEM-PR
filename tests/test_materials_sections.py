import unittest

import numpy as np

from material.elastic import Elastic
from material.steel01 import Steel01
from section.aggregator import Aggregator
from section.elasticSection import ElasticSection


class MaterialTests(unittest.TestCase):
    def test_elastic_compute_updates_trial_state(self):
        material = Elastic("mat", E=200.0)

        stress, tangent = material.compute(0.01)

        self.assertEqual(stress, 2.0)
        self.assertEqual(tangent, 200.0)
        self.assertEqual(material.getStress(), 2.0)
        self.assertEqual(material.getTangent(), 200.0)

    def test_material_state_commit_and_revert(self):
        material = Elastic("mat", E=100.0)

        material.compute(0.02)
        material.state.commit()
        material.compute(0.05)
        material.state.revert()

        self.assertEqual(material.state.strain, 0.02)
        self.assertEqual(material.state.stress, 2.0)
        self.assertEqual(material.state.tangent, 100.0)

    def test_steel01_is_elastic_before_yield(self):
        material = Steel01("steel", fy=450.0, E0=210000.0, b=0.01)

        stress, tangent = material.compute(0.001)

        self.assertAlmostEqual(stress, 210.0)
        self.assertAlmostEqual(tangent, 210000.0)


class SectionTests(unittest.TestCase):
    def test_elastic_section_force_and_stiffness(self):
        section = ElasticSection("sec", E=2.0, A=3.0, I=5.0)

        section.setSectionDeformations(np.array([[0.1], [0.2]]))

        np.testing.assert_allclose(
            section.getSectionStiffness(),
            np.array([[6.0, 0.0], [0.0, 10.0]]),
        )
        np.testing.assert_allclose(
            section.getSectionForces(),
            np.array([[0.6], [2.0]]),
        )

    def test_aggregator_uses_independent_material_copies(self):
        axial = Elastic("axial", E=10.0)
        bending = Elastic("bending", E=20.0)
        section = Aggregator("sec", axial.getCopy(), bending.getCopy())

        section.setSectionDeformations(np.array([[0.3], [0.4]]))

        np.testing.assert_allclose(section.getSectionForces(), np.array([[3.0], [8.0]]))
        np.testing.assert_allclose(
            section.getSectionStiffness(),
            np.array([[10.0, 0.0], [0.0, 20.0]]),
        )
        self.assertEqual(axial.getStress(), 0.0)
        self.assertEqual(bending.getStress(), 0.0)


if __name__ == "__main__":
    unittest.main()
