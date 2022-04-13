import os
import constants as c
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import numpy as np
from contiguous import find_contiguous

class ROBOT:
    def __init__(self, id: str, gen: str) -> None:
        self.id = id
        self.gen = gen

        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain-{id}-{gen}.nndf")
        os.system(f"rm brain-{id}-{gen}.nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.sense_hist = []

    def get_fitness(self):
        x, y, z = p.getLinkState(self.robotId, 0)[0]

        flying = np.asarray(self.sense_hist) == -4;

        values, _, lens = find_contiguous(flying)
        potentials = lens[values == True]
        best = 0
        if len(potentials) > 0:
            best = potentials.max()
        return best
        # return self.cum_fitness

    def get_phenotype(self):
         x, y, z = p.getLinkState(self.robotId, 0)[0]
         fitness = self.get_fitness()
         return {
             "species": self.id,
             "gen": self.gen,
             "x": x,
             "y": y,
             "z": z,
             "fitness": fitness,
             "sense_hist": self.sense_hist
         }



    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(self.robotId, jointName)

    def sense(self, t):
        for (linkName, sensor) in self.sensors.items():
            sensor.values[t] = sensor.getValue()
        self.sense_hist.append(np.asarray(self.nn.get_sensor_neuron_values()).sum())

    def think(self, t):
        self.nn.Update()

    def act(self, t):
        for neuron in self.nn.neurons.values():
            if(neuron.Is_Motor_Neuron()):
                jointName = neuron.Get_Joint_Name()
                desiredAngle = neuron.Get_Value() * c.motorJointRange
                self.motors[jointName].update(desiredAngle)
