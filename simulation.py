from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.world = WORLD()
        self.robot = ROBOT()

    def run(self):
        for t in range(c.simulationSteps):
            p.stepSimulation()

            self.robot.sense(t)
            self.robot.think(t)
            self.robot.act(t)

    def __del__(self):
        p.disconnect()