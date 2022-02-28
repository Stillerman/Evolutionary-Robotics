import pybullet as p
import constants as c

class WORLD:
    def __init__(self):

        p.setGravity(0,0,c.gravity)
        self.planeId = p.loadURDF("plane.urdf")

        p.loadSDF("world.sdf")