from simulation import SIMULATION
import os
import sys
import numpy as np
import json

id = sys.argv[1]
gen = sys.argv[2]

simulation = SIMULATION()
simulation.run()
print("Fitness", simulation.get_fitness())

def convert(o):
    if isinstance(o, np.generic): return o.item()
    raise TypeError

with open(f"phenotypes/pheno-gen-{gen}-species-{id}.json", "w") as f:
    # f.write("fitness:" + str(simulation.get_fitness()))
    f.write(json.dumps(simulation.get_phenotype(), default=convert))
