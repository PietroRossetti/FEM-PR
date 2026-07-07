import unittest

from model import Model


class ModelDomainTests(unittest.TestCase):
    def test_model_factories_register_objects(self):
        model = Model()

        node_i = model.node(1, 0.0, 0.0)
        node_j = model.node(2, 1.0, 0.0)
        material = model.material("elastic", "mat", 100.0)
        section = model.section("elasticSection", "sec", 100.0, 2.0, 3.0)
        beam_integration = model.beamIntegration("legendre", "int", 2, "sec")
        transformation = model.geomTransf("linear", "lin")
        element = model.element("dispBeamColumn", "ele", 1, 2, "lin", "int")

        self.assertIs(model.getNode(1), node_i)
        self.assertIs(model.getNode(2), node_j)
        self.assertIs(model.getMaterial("mat"), material)
        self.assertIs(model.getSection("sec"), section)
        self.assertIs(model.getBeamIntegration("int"), beam_integration)
        self.assertIs(model.getGeomTransf("lin"), transformation)
        self.assertIs(model.getElement("ele"), element)

    def test_duplicate_ids_are_rejected(self):
        model = Model()
        model.node(1, 0.0, 0.0)

        with self.assertRaisesRegex(ValueError, "already contains node"):
            model.node(1, 1.0, 0.0)

    def test_missing_ids_and_unknown_factory_types_are_rejected(self):
        model = Model()

        with self.assertRaisesRegex(KeyError, "does not contain node"):
            model.getNode("missing")
        with self.assertRaisesRegex(ValueError, "Unknown material type"):
            model.material("unknown", 1)
        with self.assertRaisesRegex(ValueError, "Unknown section type"):
            model.section("unknown", 1)
        with self.assertRaisesRegex(ValueError, "Unknown integration type"):
            model.beamIntegration("unknown", 1)
        with self.assertRaisesRegex(ValueError, "Unknown geometric"):
            model.geomTransf("unknown", 1)
        with self.assertRaisesRegex(ValueError, "Unknown element type"):
            model.element("unknown", 1)


if __name__ == "__main__":
    unittest.main()
