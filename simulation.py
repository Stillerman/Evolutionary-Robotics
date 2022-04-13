from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import sys

class SIMULATION:
    def __init__(self):
        self.id = sys.argv[1]
        self.gen = sys.argv[2]
        print ("SIMULATING", self.id, self.gen)
        
        mode = p.DIRECT if sys.argv[3].lower() == "direct" else p.GUI

        self.physicsClient = p.connect(mode)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.world = WORLD()
        self.robot = ROBOT(self.id, self.gen)

    def run(self):
        for t in range(c.simulationSteps):
            p.stepSimulation()

            self.robot.sense(t)
            self.robot.think(t)
            self.robot.act(t)

    def __del__(self):
        p.disconnect()

    def get_fitness(self):
        return self.robot.get_fitness()

    def get_phenotype(self):
        return self.robot.get_phenotype()
