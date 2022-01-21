import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")

# Size = l,w,h

for x in range(6):
    for y in range(6):
        l = 1
        total = 0
        for i in range(10):
            pyrosim.Send_Cube(name="Box" + str(i), pos=[x,y,total + 0.5] , size=[l,l,l])
            total += l
            l = l * 0.9


pyrosim.End()
