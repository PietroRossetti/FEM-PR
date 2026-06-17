from material import *
from node import Node
from model import Model

elastic = Elastic(1,1000)

eps = [0., 0.001, 0.002, 1.]

sig, E = elastic.materialTester(eps)

for sigi, Ei in zip(sig,E):
    print("sig: ",sigi,"E: ", Ei)

print()
print("-"*100)
steel = Steel01(2,300.,1000.,0.05)

sig, E = steel.materialTester(eps)

for sigi, Ei in zip(sig,E):
    print("sig: ",sigi,"E: ", Ei)


n1 = Node(1,0.,1.,2.)

x,y,z = n1.getCoord()
print()
print("-"*100)
print(x,y,z)

m = Model()
m.material("steel01",1,450,210000,0.005)
print(m.materials)
m.section("aggregator",1,1,1)
print(m.sections[1].sectionState)