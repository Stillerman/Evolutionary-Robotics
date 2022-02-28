import numpy as np
import constants as c
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, robotId, jointName) -> None:
        self.jointName = jointName
        self.robotId = robotId

        self.amplitude, self.frequency, self.phaseOffset = np.pi/4, 40, 0

        if self.jointName == "Torso_BackLeg":
            self.frequency /= 2

        linSpace = np.linspace(0, 2*np.pi, c.simulationSteps)
        self.targetAngles = self.amplitude * np.sin(self.frequency * linSpace + self.phaseOffset)

        pass

    def update(self, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = self.robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.targetAngles[t],
            maxForce = 50 # 500 NM
        )