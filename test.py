from material import *


elastic = Elastic(1,1000)

eps = [0., 0.1, 0.2, 1.]

sig, E = elastic.materialTester(eps)

for sigi, Ei in zip(sig,E):
    print("sig: ",sigi,"E: ", Ei)