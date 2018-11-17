import random
import math

class Neuron:
    inputSum = 0
    weight = 0
    bias = 5

    def mutate(self):
        self.weight += random.random()

    def __init__(self,inputSum,weight):
        self.inputSum = inputSum
        self.weight = weight
        self.mutate()

    def run(self):
        if (round(self.inputSum*self.weight - self.bias)):
            return True
        return False
