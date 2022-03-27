from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self) -> None:
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain.nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def get_fitness(self):
        x, y, z = p.getLinkState(self.robotId, 0)[0]
        return x

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

    def think(self, t):
        self.nn.Update()
        self.nn.Print()

    def act(self, t):
        for neuron in self.nn.neurons.values():
            if(neuron.Is_Motor_Neuron()):
                jointName = neuron.Get_Joint_Name()
                desiredAngle = neuron.Get_Value()
                self.motors[jointName].update(desiredAngle)
