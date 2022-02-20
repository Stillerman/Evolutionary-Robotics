import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import random
import numpy as np
import math

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

TICKS = 10000
STEPS = 5

backLegHist = np.zeros(TICKS)
frontLegHist = np.zeros(TICKS)

def randAngle():
	return random.uniform(-math.pi/2, math.pi/2)


# mplitude, frequency, and phaseOffset at the top of your code. Set their values to pi/4, 1 and 0 respectively for now.
amplitude_f, frequency_f, phaseOffset_f = np.pi/4, 40, 0
amplitude_b, frequency_b, phaseOffset_b = np.pi/4, 40, np.pi/4

linSpace = np.linspace(0, 2*np.pi, TICKS)
targetAngles_f = amplitude_f * np.sin(frequency_f * linSpace + phaseOffset_f)
targetAngles_b = amplitude_b * np.sin(frequency_b * linSpace + phaseOffset_b)

for i in range(TICKS):
	p.stepSimulation()
	backLegHist[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegHist[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

	pyrosim.Set_Motor_For_Joint(
		bodyIndex = robotId,
		jointName = "Torso_BackLeg",
		controlMode = p.POSITION_CONTROL,
		targetPosition = targetAngles_b[i],
		maxForce = 50 # 500 NM
	)

	pyrosim.Set_Motor_For_Joint(
		bodyIndex = robotId,
		jointName = "Torso_FrontLeg",
		controlMode = p.POSITION_CONTROL,
		targetPosition = targetAngles_f[i],
		maxForce = 50 # 500 NM
	)
	# time.sleep(1/1000)

np.save("data/backLegSensorValues.npy", backLegHist)
np.save("data/frontLegSensorValues.npy", frontLegHist)
np.save("data/targetAngles_f.npy", targetAngles_f)
np.save("data/targetAngles_b.npy", targetAngles_b)

p.disconnect()