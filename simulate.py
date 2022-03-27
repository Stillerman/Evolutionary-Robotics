from simulation import SIMULATION
import os

simulation = SIMULATION()
simulation.run()
print("Fitness", simulation.get_fitness())
with open("fitness.txt", "w") as f:
    f.write("fitness:" + str(simulation.get_fitness()))
