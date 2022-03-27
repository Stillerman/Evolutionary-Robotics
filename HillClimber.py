#!/usr/bin/env python


from solution import Solution
from copy import deepcopy

class HillClimber:
    def __init__(self):
        self.parent = Solution()
        print("Init Hill climber")
        self.parent.evaluate(show=True)
        self.evolve()

    def evolve(self):
        for i in range(15):
            fit = self.evolve_one_gen()
            print(f"Gen {i} done with fitness {fit}")

        self.parent.evaluate(show=True)

    def evolve_one_gen(self):
        # print("\t Evaluating Parent")
        p_fit = self.parent.evaluate(show=False)


        self.child = deepcopy(self.parent)
        # print("Child Weights b4")
        # print(self.child.weights)
        self.child.mutate()
        # print("Child weights after")
        # print(self.child.weights)

        # print("\t Evaluating Child")
        c_fit = self.child.evaluate(show=False)

        print("p_fit", p_fit, "c_fit", c_fit)

        if (c_fit > p_fit):
            # print("Child out-performed parent")
            self.parent = deepcopy(self.child)
            return c_fit

        # print("Parent out-preformed child")
        return p_fit
