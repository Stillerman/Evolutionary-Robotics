#!/usr/bin/env python
import numpy as np
import time
from numpy.random import randint, random
import pyrosim.pyrosim as pyrosim
import os


class Solution:
    def __init__(self):
        self.weights = np.random.rand(3, 2) * 2 - 1
        self.setup()

    def mutate(self):
        row = randint(0,3)
        col = randint(0,2)
        self.weights[row, col] = random() * 2 - 1
        self.setup()

    def evaluate(self, show=False):
        self.setup()
        # print("evaluating with weights", self.weights)
        os.system(f"python simulate.py {'GUI' if show else 'DIRECT'} > /dev/null 2> /dev/null")
        time.sleep(0.5)
        with open("fitness.txt", "r") as f:
            line = f.readline()
            _, fStr = line.split(":")
            return float(fStr)

    def setup(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])

        pyrosim.Send_Joint(
            name="Torso_BackLeg",
            parent="Torso",
            child="BackLeg",
            type="revolute",
            position=[-0.5, 0, 1],
        )
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

        pyrosim.Send_Joint(
            name="Torso_FrontLeg",
            parent="Torso",
            child="FrontLeg",
            type="revolute",
            position=[0.5, 0, 1],
        )
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for sensor_idx in [0, 1, 2]:
            for motor_idx in [0, 1]:
                pyrosim.Send_Synapse(
                    sourceNeuronName=sensor_idx,
                    targetNeuronName=motor_idx + 3,
                    weight=self.weights[sensor_idx, motor_idx],
                )

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()
