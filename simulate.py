import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegHist = np.zeros(1000)
frontLegHist = np.zeros(1000)

for i in range(1000):
	p.stepSimulation()
	backLegHist[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegHist[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

	pyrosim.Set_Motor_For_Joint(
		bodyIndex = robotId,
		jointName = "Torso_BackLeg",
		controlMode = p.POSITION_CONTROL,
		targetPosition = 0.0,
		maxForce = 500 # 500 NM
	)
	time.sleep(1/600)

np.save("data/backLegSensorValues.npy", backLegHist)
np.save("data/frontLegSensorValues.npy", frontLegHist)

p.disconnect()