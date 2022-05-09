#!/usr/bin/env python


from solution import Solution
from copy import deepcopy
import os

# class ParallelHillClimber:
#     def __init__(self):
#         soln1 = Solution(id=0, gen=0)
#         soln1.evaluate()
#         fitness = soln1.wait_for_sim_to_end()

#         soln2 = deepcopy(soln1)
#         soln2.mutate()
#         soln2.evaluate()

#         fitness2 = soln2.wait_for_sim_to_end()

#         print(fitness, fitness2)

class ParallelHillClimber:
    def __init__(self, popSize=20, useHidden=True):
        self.parents = {}
        self.parentsFitness = {}
        self.popSize = popSize
        print("Init Parallel Hill climber")
        for i in  range(self.popSize):
            self.parents[i] = Solution(id = str(i) + "-" + ("hidden" if useHidden else "no-hidden"), gen = 0, useHidden=useHidden)

        # self.parent.evaluate(show=True)
        self.evolve()

    def evolve(self):
        # print("pre")
        for i, parent in self.parents.items():
            # print("Evaluing", i)
            parent.evaluate(show=False, debug = False)


        for i, parent in self.parents.items():
            fitness = parent.wait_for_sim_to_end()
            print(f"{i}'s fitness: {fitness}")
            self.parentsFitness[i] = fitness

        children = {}
        childrensFitness = {}

        for gen in range(1, 25):
            # input(f"Train Gen {gen}?")
            print(f"\t\t GEN - {gen}")
            
            for pid, parent in self.parents.items():
                children[pid] = deepcopy(parent)
                children[pid].mutate(gen)

            for i, child in children.items():
                child.evaluate(show=False, debug=False)

            for i, child in children.items():
                fitness = child.wait_for_sim_to_end()
                # print(f"{i}'s fitness: {fitness} (child)")
                childrensFitness[i] = fitness

            for (i, pfit) in self.parentsFitness.items():
                cfit = childrensFitness[i]
                if cfit > pfit:
                    print (f"Child {i} outperformed parent")
                    self.parents[i] = children[i]
                    self.parentsFitness[i] = childrensFitness[i]

            for i, fitness in self.parentsFitness.items():
                print(f"Species {i}'s fitness: {fitness}")

        bestFitness = -100
        bestParent = -1
        for i, fit in self.parentsFitness.items():
            if fit > bestFitness:
                bestFitness = fit
                bestParent = i

        print(f"Showing species {bestParent} with fitness {bestFitness}")
        self.parents[bestParent].evaluate(show=True, debug=False)
        # for i in range(15):
        #     fit = self.evolve_one_gen()
        #     print(f"Gen {i} done with fitness {fit}")

        # self.parent.evaluate(show=True)

    # def evolve_one_gen(self):
    #     # print("\t Evaluating Parent")
    #     p_fit = self.parent.evaluate(show=False)


    #     self.child = deepcopy(self.parent)
    #     # print("Child Weights b4")
    #     # print(self.child.weights)
    #     self.child.mutate()
    #     # print("Child weights after")
    #     # print(self.child.weights)

    #     # print("\t Evaluating Child")
    #     c_fit = self.child.evaluate(show=False)

    #     print("p_fit", p_fit, "c_fit", c_fit)

    #     if (c_fit > p_fit):
    #         # print("Child out-performed parent")
    #         self.parent = deepcopy(self.child)
    #         return c_fit

    #     # print("Parent out-preformed child")
    #     return p_fit
