#!/usr/bin/env python
import json
import numpy as np
import time
from numpy.random import randint, random
import pyrosim.pyrosim as pyrosim
import os
import constants as c


class Solution:
    def __init__(self, id: str, gen: int):
        self.id = id
        self.gen = gen
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.setup()

    def mutate(self, gen):
        row = randint(0, c.numSensorNeurons)
        col = randint(0, c.numMotorNeurons)
        self.weights[row, col] = random() * 2 - 1
        self.gen = gen
        self.setup()

    def evaluate(self, show=False, debug = False):
        self.setup()
        # print("evaluating with weights", self.weights)
        os.system(f"rm phenotypes/pheno-gen-{self.gen}-species-{self.id}.json")
        os.system(
            f"python simulate.py {self.id} {self.gen} {'GUI' if show else 'DIRECT'} {'> /dev/null 2> /dev/null' if not debug else ''} &"
        )

    def wait_for_sim_to_end(self):
        fitnessFileName = f"phenotypes/pheno-gen-{self.gen}-species-{self.id}.json"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.1)
            # print("waiting for", fitnessFileName)

        time.sleep(0.1)
        with open(fitnessFileName, "r") as f:
            phenotype = json.load(f)
            return float(phenotype["fitness"])
            # line = f.readline()
            # _, fStr = line.split(":")
            # return float(fStr)

    def setup(self):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])

        pyrosim.Send_Joint(
            name="Torso_BackLeg",
            parent="Torso",
            child="BackLeg",
            type="revolute",
            position=[0, -0.5, 1],
            jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.25, 1, 0.25])

        # LowerBack
        pyrosim.Send_Joint(
            name="BackLeg_LowerBackLeg",
            parent="BackLeg",
            child="LowerBackLeg",
            type="revolute",
            position=[0,-1,0],
            jointAxis="1 0 0"
        )

        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0,0,-0.5], size=[0.25,0.25,1])

        # End LowerBack

        pyrosim.Send_Joint(
            name="Torso_FrontLeg",
            parent="Torso",
            child="FrontLeg",
            type="revolute",
            position=[0, 0.5, 1],
            jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.25, 1, 0.25])

        pyrosim.Send_Joint(
            name="FrontLeg_LowerFrontLeg",
            parent="FrontLeg",
            child="LowerFrontLeg",
            type="revolute",
            position=[0,1,0],
            jointAxis="1 0 0"
        )

        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[0,0,-0.5], size=[0.25,0.25,1])

        pyrosim.Send_Joint(
            name="Torso_LeftLeg",
            parent="Torso",
            child="LeftLeg",
            type="revolute",
            position=[-0.5, 0, 1],
            jointAxis="0 1 0"
        )

        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.25, 0.25])

        # Lower Left Leg
        pyrosim.Send_Joint(
            name="LeftLeg_LowerLeftLeg",
            parent="LeftLeg",
            child="LowerLeftLeg",
            type="revolute",
            position=[-1,0,0],
            jointAxis="0 1 0"
        )

        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0,0,-0.5], size=[0.25,0.25,1])

        # Right
        pyrosim.Send_Joint(
            name="Torso_RightLeg",
            parent="Torso",
            child="RightLeg",
            type="revolute",
            position=[0.5, 0, 1],
            jointAxis="0 1 0"
        )

        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.25, 0.25])

        # Lower Right Leg
        pyrosim.Send_Joint(
            name="RightLeg_LowerRightLeg",
            parent="RightLeg",
            child="LowerRightLeg",
            type="revolute",
            position=[1,0,0],
            jointAxis="0 1 0"
        )

        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0,0,-0.5], size=[0.25,0.25,1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain-{self.id}-{self.gen}.nndf")
        # pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        # pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        # pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LowerRightLeg")

        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="BackLeg_LowerBackLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_LowerRightLeg")

        for sensor_idx in range(c.numSensorNeurons):
            for motor_idx in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=sensor_idx,
                    targetNeuronName=motor_idx + c.numSensorNeurons,
                    weight=self.weights[sensor_idx, motor_idx],
                )

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()
