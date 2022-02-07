import numpy as np
import matplotlib.pyplot as plt

bls = np.load("data/backLegSensorValues.npy")
fls = np.load("data/frontLegSensorValues.npy")

plt.plot(bls, label = "Back leg", linewidth = 4)
plt.plot(fls, label = "Front leg")
plt.legend()
plt.show()