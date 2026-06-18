from material import *
import matplotlib.pyplot as plt
import numpy as np
from node import Node

from model import Model

# ---------------------------------------
# test MATERIAL
# ---------------------------------------
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

eS = r"$\epsilon$"
sS = r"$\sigma$"
plt.figure()
plt.plot(np.arange(1,1+len(eps)) ,eps)
plt.xlabel("step ID")
plt.ylabel(eS)
plt.title("cyclic path")
plt.grid("on")
plt.figure()
plt.plot(eps,sig)
plt.xlabel(eS)
plt.ylabel(sS)
plt.title("steel01")
plt.grid("on")
#plt.show()


# ---------------------------------------
# test NODE
# ---------------------------------------

n1 = Node(1,0.,1.,2.)
x,y,z = n1.getCoord()
print()
print("-"*100)
print(x,y,z)

# ---------------------------------------
# test MODEL
# ---------------------------------------

m = Model()
m.material("steel01","steel",450,210000,0.005)
print(m.materials)
m.section("aggregator","agg","steel","steel")

m.beamIntegration("lobatto","beamIntID",5,"agg")


print("-"*50)
print("MATERIALS:")
for k,v in m.materials.items():
    print(k," : ",v.id)

print("SECTIONS:")
for k,v in m.sections.items():
    print(k," : ",v.id)

print("BEAM INTEGRATIONS:")
for k,v in m.beamIntegrations.items():
    print(k," : ",v.id)



t = 1