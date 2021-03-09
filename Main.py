import pygame
import math
from pygame import gfxdraw
import random

#[A-Z]
alpha = ''.join([chr(x) for x in range(65,91)])

# gravitational constant
G = 6.67408 * (10 ** -11)

# colours for use
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
YELLOW = (255,255, 0)
GREY  = ( 30, 30, 30)

# list of colours for random colours
colours = (WHITE, RED, GREEN, BLUE, GREY)

G = 6.67408 * (10 ** -11)

# defining vector2D
# using vector2D as it is what im used to in C#
vector2D = pygame.math.Vector2

class BODY():
    '''
    class for creating planetary bodies
    '''
    def __init__(self, win, mass, radius, pos, vel, colour, name, stationary = False, drawTrail = False):
        # name of the object/planet/body
        self.name = name
        # window to draw to 
        self.win = win
        # mass of the planet
        self.mass = mass
        # if name of the body is Sun then I decrease radius
        # this is to fit it on my model of solar system
        # comment this out if you want dont want to model the solar system
        if self.name == "Sun":
            self.radius = radius / 10
        else:
            self.radius = radius
        # 2D vector of the position of the planet
        self.pos = vector2D(pos)
        # 2D vector for velocity and acceleration
        # we update acceleration then update velocity based on acceleration
        self.vel = vector2D(vel)
        self.acceleration = vector2D(0,0)
        # colour of the planet
        self.colour = colour
        # whether we want it to be stationary
        # like the sun being in the middle of the screeen
        self.stationary = stationary
        # delete the body
        # we set to False because we dont want to delete the body
        self.dele = False

        # to draw the planets
        self.posToScreen = 1_000_000_000
        self.radiusScaler = 10_000_000

        self.drawTrail = drawTrail
        self.fullCircle = True
        if self.drawTrail:
            self.points = []

    def updateVel(self, others):
        '''
        update the velocity using the newtonian gravity equation
        F = G * (m1 * m2)/r^2
        
        F  = force
        G  = gravitational constant
        m1 = mass of object 1
        m2 = mass of object 2
        r  = distance between object 1 and object 2
        '''
        for other in others:
            if self != other:
                r = (other.pos - self.pos).length()
                direc  = (other.pos - self.pos).normalize()
                force = direc * G * self.mass * other.mass / (r * r)
                # code to stop updating dead planet 
                if self.dele or self.mass == 0:
                    return
                # dividing by this mass cancels out multiplying in the above equation
                # keeping to make easier to understand
                #  F = MA
                #  A = F/M
                acc = force / self.mass
                self.vel += acc * 100000
                
    def delete(self):
        '''
        function to delete to the body
        if certain parameters are met
        change here depending on what you want
        '''
        # positions to great
        if self.pos.x > 10000 or self.pos.y > 10000:
            self.dele = True
            return True
        # velocity to great
        if self.vel.x > 10000 or self.vel.y > 10000:
            self.dele = True
            return True
        # mass = 0
        # only occurs if using morph function
        if self.mass == 0:
            self.dele = True
            return True
        return False

    def morph(self, other):
        '''
        function to morph two planets into one
        still buggy
        '''
        # if the distance between the two planets
        # we morph them to the bigger planet
        if (self.pos - other.pos).length() < self.mass // self.radiusScaler:
            # choosing which planet to add other mass to
            if self.mass > other.mass:
                self.mass += other.mass
                self.vel = vector2D(0,0)
                other.mass = 0
            else:
                other.mass += self.mass
                other.vel = vector2D(0,0)
                self.mass = 0
        return

    def updatePos(self, delta):
        '''
        update position based on velocity
        two seperate functions:
            - one to add to the velocity based on gravity and acceleration
            - one to add velocity to position
        this is so the forces dont ripple and are all calculated at the same time
        '''
        # only updates if it isnt stationary
        if not self.stationary:
            # adding veloctiy to position times by time delta
            # time delta is the difference between frames
            # creates smooth movement even if Frames Per Second is different
            self.pos += self.vel * delta * 100000
            if self.drawTrail:
                self.points.append((self.pos.x / self.posToScreen, self.pos.y / self.posToScreen))
                if len(self.points) > 1000 and not self.fullCircle:
                    self.points = self.points[10:]

    def show(self):
        # draw a filled circle with a radius being scaled
        gfxdraw.filled_circle(self.win, int(self.pos.x / self.posToScreen), int(self.pos.y / self.posToScreen), int(self.radius / self.radiusScaler), self.colour)
        if self.drawTrail and len(self.points) > 2:
            colour = [self.colour[0] - 70 if self.colour[0] > 70 else 0, self.colour[1] - 70 if self.colour[1] > 70 else 0, self.colour[2] - 70 if self.colour[2] > 70 else 0]
            pygame.draw.lines(self.win, colour, False, self.points, 1)

