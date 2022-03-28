from simulation import SIMULATION
import os
import sys

id = sys.argv[1]
simulation = SIMULATION()
simulation.run()
print("Fitness", simulation.get_fitness())
with open(f"fitness-{id}.txt", "w") as f:
    f.write("fitness:" + str(simulation.get_fitness()))
