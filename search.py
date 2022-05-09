import os
from ParallelHillClimber import ParallelHillClimber

#for i in range(5):
#    os.system("python generate.py")
#    os.system("python simulate.py")

# hc = HillClimber()
one = ParallelHillClimber(popSize=20, useHidden=True)
two = ParallelHillClimber(popSize=20, useHidden=False)
