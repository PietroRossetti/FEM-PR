from material import *
import matplotlib.pyplot as plt
import numpy as np
from node import Node

from model import Model

# ---------------------------------------
# test MATERIAL
# ---------------------------------------
'''
nCycle = 4
epsU = 0.005

eps_list = []
lastEps = 0

for i in range(1, nCycle + 1):

    for j in [1, -1]:

        epsCycle = (epsU / nCycle)*i*j
        c = np.linspace(lastEps, epsCycle, 100)

        eps_list.append(c)
        lastEps = epsCycle

c = np.linspace(lastEps, 0, 100)
eps_list.append(c)
eps = np.concatenate(eps_list)


elastic = Elastic(1,1000)
sig, E = elastic.materialTester(eps)

steel = Steel01(2,450.,2.1e5, 0.005)
sig, E = steel.materialTester(eps)
print(sig[-1])


# PLOT
plt.figure()
plt.plot(np.arange(1,1+len(eps)) ,eps)
plt.xlabel("step ID")
plt.ylabel("eps")
plt.title("cyclic path")
plt.grid("on")
plt.figure()
plt.plot(eps,sig)
plt.xlabel("eps")
plt.ylabel("sigma")
plt.title("steel01")
plt.grid("on")
plt.show()
'''
# ---------------------------------------
# test MODEL
# ---------------------------------------

m = Model()
m.node(1,0.,0.)
m.node(2,0.,1.)
m.material("steel01","mat1",450,210000,0.005)
m.section("aggregator","sec1","mat1","mat1")
m.section("elasticSection","sec2", 1, 10, 1)
m.beamIntegration("lobatto","beamInt1",5,"sec2")
m.geomTransf("linear","linearTransf")
ele = m.element("dispBeamColumn","BBC",1,2,"linearTransf","beamInt1")

# test nonlinear bispBeamColumn
m.material("steel01","bendingID",1e10 , 1., 0.005)
m.material("steel01","axialID",1e10 , 10 , 0.005)
m.section("aggregator","beamSection","axialID","bendingID")
m.beamIntegration("lobatto","beamInt2",5,"beamSection")
beam = m.element("dispBeamColumn","nonlinearDBC",1,2,"linearTransf","beamInt2")




print("-"*50)
print("NODES:")
for k,v in m.nodes.items():
    print(k,v)

print("MATERIALS:")
for k,v in m.materials.items():
    print(k," : ",v.id)

print("SECTIONS:")
for k,v in m.sections.items():
    print(k," : ",v.id)

print("BEAM INTEGRATIONS:")
for k,v in m.beamIntegrations.items():
    print(k," : ",v.id)

print("GEOMETRIC TRANSFORMATIONS:")
for k,v in m.geometricTransformations.items():
    print(k," : ",v.id)

print("ELEMENTS:")
for k,v in m.elements.items():
    print(k,v)
'''
print("\n","-"*100)
print(ele.initialLength)
u = np.array([[0,1,0,0,0,0]]).T
ele.setTrialDisp(u)
k = ele.getEleStiffness()
T = ele.geomTransf.getTransfMatrix() # rotation matrix
kloc = T.T @ k @ T
print("k global:\n", k)
print("k local:\n", kloc)
print("F global from element:\n", ele.getEleForces())
print("F global from k @ u:\n", k @ u)
'''
u = np.array([[0,1,0,0,0,0]]).T
print("\n","-"*100)

m.getNode(1).state.disp = u[0:3].copy()
m.getNode(2).state.disp = u[3:6].copy()
beam.setElementDeformations()

k = beam.getElementStiffness()
T = beam.geomTransf.getTransfMatrix() # rotation matrix
kloc = T @ k @ T.T
print("k global:\n", k)
print("k local:\n", kloc)
print("F global from element:\n", beam.getElementForces())
print("F global from k @ u:\n", k @ u)
