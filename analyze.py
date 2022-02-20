import numpy as np
import matplotlib.pyplot as plt

bls = np.load("data/backLegSensorValues.npy")
fls = np.load("data/frontLegSensorValues.npy")

targetAngles_f = np.load("data/targetAngles_f.npy")
targetAngles_b = np.load("data/targetAngles_b.npy")

# plt.plot(bls, label = "Back leg", linewidth = 4)
# plt.plot(fls, label = "Front leg")

plt.plot(targetAngles_f, label="TA Front")
plt.plot(targetAngles_b, label="TA Back")
plt.legend()
plt.show()