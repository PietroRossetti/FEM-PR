import numpy as np

from model import Model


def main() -> None:
    m = Model()
    m.node(1, 0.0, 0.0)
    m.node(2, 0.0, 1.0)

    m.material("steel01", "mat1", 450, 210000, 0.005)
    m.section("aggregator", "sec1", "mat1", "mat1")
    m.section("elasticSection", "sec2", 1, 10, 1)
    m.beamIntegration("lobatto", "beamInt1", 5, "sec2")
    m.geomTransf("linear", "linearTransf")
    m.element("dispBeamColumn", "BBC", 1, 2, "linearTransf", "beamInt1")

    m.material("steel01", "bendingID", 1e10, 1.0, 0.005)
    m.material("steel01", "axialID", 1e10, 10, 0.005)
    m.section("aggregator", "beamSection", "axialID", "bendingID")
    m.beamIntegration("lobatto", "beamInt2", 5, "beamSection")
    beam = m.element("dispBeamColumn", "nonlinearDBC", 1, 2, "linearTransf", "beamInt2")

    print("-" * 50)
    print("NODES:")
    for key, value in m.nodes.items():
        print(key, value)

    print("MATERIALS:")
    for key, value in m.materials.items():
        print(key, " : ", value.id)

    print("SECTIONS:")
    for key, value in m.sections.items():
        print(key, " : ", value.id)

    print("BEAM INTEGRATIONS:")
    for key, value in m.beamIntegrations.items():
        print(key, " : ", value.id)

    print("GEOMETRIC TRANSFORMATIONS:")
    for key, value in m.geometricTransformations.items():
        print(key, " : ", value.id)

    print("ELEMENTS:")
    for key, value in m.elements.items():
        print(key, value)

    u = np.array([[0, 1, 0, 0, 0, 0]]).T
    m.getNode(1).state.disp = u[0:3].copy()
    m.getNode(2).state.disp = u[3:6].copy()
    beam.setElementDeformations()

    k = beam.getElementStiffness()
    transform = beam.geomTransf.getTransfMatrix()
    k_local = transform @ k @ transform.T

    print("\n", "-" * 100)
    print("k global:\n", k)
    print("k local:\n", k_local)
    print("F global from element:\n", beam.getElementForces())
    print("F global from k @ u:\n", k @ u)


if __name__ == "__main__":
    main()
