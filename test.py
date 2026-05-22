from material import *


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

