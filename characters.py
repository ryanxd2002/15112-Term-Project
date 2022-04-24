from cmu_112_graphics import *
import math, random, numpy as np
################################################################################
################################################################################

class Drone:
    def __init__(self, x0, x1):

        # Create random number
        randomNumber = random.randint(30, 50)

        # Take in patrol range
        self.patrolPoint1 = x0
        self.patrolPoint2 = x1

        # Take spawn point
        self.spawn = (x0 + x1) // 2

        self.size = randomNumber

        # Body coords
        self.body = [self.spawn - self.size,
                     150 + self.size, 
                     self.spawn + self.size, 
                     150 - self.size]
        
        # Eye coords
        self.eye = [self.spawn - self.size ,
                     150 + self.size , 
                     self.spawn + self.size , 
                     150 - self.size]

        # Pupil coords
        self.pupil = [self.spawn - (self.size // 2),
                     150, 
                     self.spawn + (self.size // 2), 
                     150 + (self.size)]

        # Scanner
        self.scanner = [self.spawn, self.spawn + self.size,
                        self.spawn - self.size,
                        self.spawn + self.size]

        self.point = []

class Spikes:
    def __init__(self, x, y):

        # Create coords
        self.coords = [(x,y), (x + 10, y - 20), (x + 20, y)] 

class Turtle:
    def __init__(self, x, y, i):

        # Take index
        self.i = i

        # Create coords
        self.coords = [[x, y - 20], [x + 20, y], [x + 10, y - 20], [x + 40, y]]

class Crusher:
    def __init__(self, x, y):

        # Create coords
        self.coords = [(x,y)]

        self.ball = [[x, y]]