from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR

class ROBOT:
    def __init__(self) -> None:
        self.robotId = p.loadURDF("body.urdf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()


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

    def act(self, t):
        for (jointName, motor) in self.motors.items():
            motor.update(t)