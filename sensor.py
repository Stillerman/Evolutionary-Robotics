import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self, linkName) -> None:
        self.linkName = linkName
        self.values = np.zeros(c.simulationSteps)

    def getValue(self):
        return pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
