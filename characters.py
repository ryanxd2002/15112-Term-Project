from cmu_112_graphics import *
import math, random, numpy as np

################################################################################
################################################################################

class Drone:
    def __init__(self, x0, x1):
        randomNumber = random.randint(30, 50)

        self.patrolPoint1 = x0
        self.patrolPoint2 = x1
        self.spawn = (x0 + x1) // 2
        self.size = randomNumber

        self.body = [self.spawn - self.size,
                     150 + self.size, 
                     self.spawn + self.size, 
                     150 - self.size]

        self.eye = [self.spawn - self.size ,
                     150 + self.size , 
                     self.spawn + self.size , 
                     150 - self.size]

        self.pupil = [self.spawn - (self.size // 2),
                     150, 
                     self.spawn + (self.size // 2), 
                     150 + (self.size)]

class Spikes:
    def __init__(self, x1, x2, numberOfSpikes):

        self.numberOfSpikes = numberOfSpikes
        

class Turtle:
    def __init__(self, x, y):
        self.beam = 0

class Crusher:
    def __init__(self, x, y):
        self.beam = 0




