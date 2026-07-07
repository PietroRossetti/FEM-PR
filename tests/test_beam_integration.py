import unittest

from beamIntegration.gaussLegendre import GaussLegendre
from beamIntegration.gaussLobatto import GaussLobatto
from section.elasticSection import ElasticSection


class BeamIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.section = ElasticSection("sec", E=1.0, A=1.0, I=1.0)

    def test_gauss_legendre_weights_integrate_constant_over_length(self):
        integration = GaussLegendre("int", 4, self.section)

        self.assertAlmostEqual(sum(integration.getWeights(3.5)), 3.5)
        self.assertEqual(len(integration.getLocations(3.5)), 4)

    def test_gauss_lobatto_weights_integrate_constant_over_length(self):
        integration = GaussLobatto("int", 5, self.section)

        self.assertAlmostEqual(sum(integration.getWeights(2.0)), 2.0)
        self.assertEqual(integration.getLocations(2.0)[0], 0.0)
        self.assertEqual(integration.getLocations(2.0)[-1], 2.0)

    def test_invalid_integration_rules_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            GaussLegendre("int", 0, self.section)
        with self.assertRaisesRegex(ValueError, "at least 2"):
            GaussLobatto("int", 1, self.section)
        with self.assertRaisesRegex(ValueError, "supports 1 to 8"):
            GaussLegendre("int", 9, self.section)
        with self.assertRaisesRegex(ValueError, "supports 2 to 8"):
            GaussLobatto("int", 9, self.section)


if __name__ == "__main__":
    unittest.main()
