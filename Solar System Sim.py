import pygame
import math
from pygame import gfxdraw
import random
from Main import BODY



# pygame colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
YELLOW = (255,255, 0)
ORANGE = (255, 69 ,0)
GREY  = ( 30, 30, 30)


MERCURY = (128,128,128)
VENUS   = (211,211,211)
EARTH   = (173,216,230)
MARS    = (153,61 ,  0)
JUPITER = (176, 127, 53)
SATURN  = (176, 143, 54)
URANUS  = (85, 128, 170)
NEPTUNE = (54, 104, 150)

colours = (WHITE, RED, GREEN, BLUE, GREY)

#G = 0.667
G = 6.67408 * (10 ** -11)

# defining vector2D
# using vector2D as it is what im used to in C#
vector2D = pygame.math.Vector2

# dimensions of the screen
WIDTH = 600
HEIGHT = 600

# init the screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()
win.fill(BLACK)

#FPS of the window
FPS = 144

def getInitialVel(dist, sunPos, bodyPos, speed):
    '''
    function to get the perpendicular vector of the position
    and turn that to a velocity based on the max speed we pass in
    '''
    xvel = (bodyPos[0] - sunPos[0]) / dist * speed
    yvel = (bodyPos[1] - sunPos[1])/ dist * speed
    
    return (yvel, -xvel)
    

def getPosFromSun(dist, sunPos, rot = False):
    '''
    get position of the planet from the sun
    using polar co-ordinates
    '''
    if rot:
        radius = dist
        # getting a random angle
        # pi * 4 being a full rotation equal to 360°
        theta = math.pi * 4 * random.random()

        # getting a normalised x and y coords
        # multiplying by radius to upscale it
        # adding sunPos to get it relative to that
        pos1 = radius * math.cos(theta) + sunPos[0]
        pos2 = radius * math.sin(theta) + sunPos[1]

        return (pos1, pos2)

    # if its not rotated
    # just spawn it to the left of the sun
    pos1 = sunPos[0] - (dist / 2)
    pos2 = sunPos[1]
    return (pos1 , pos2)

def bodyGen(dictio, name, sunPos, stat = False, rot = True, drawTrail = False):
    '''
    function to generate planets or bodies
    '''
    if name != "Sun":
        bodyPos = getPosFromSun(dictio["dist"], sunPos, rot = True)
        bodyVel = getInitialVel(dictio["dist"], sunPos, bodyPos, dictio["speed"])
        
        body = BODY(win, dictio["mass"], dictio["radius"], bodyPos, bodyVel, dictio["colour"], name, stationary = stat, drawTrail = drawTrail)
        return body
    body = BODY(win, dictio["mass"], dictio["radius"], sunPos, (0,0), dictio["colour"], name, stationary = stat, drawTrail = drawTrail)
    return body

# conversions
# makes it easier when copying facts from wiki
million = 1_000_000
billion = 1_000_000_000
km = 1000

# planet = {"dist": , "radius": , "mass": , "speed": , "colour"}
# dictionaries for the planets
sunData   = {"dist": 0, "radius": 696_340 * km, "mass": 1.989 * (10 ** 30), "speed": (0, 0), "colour": YELLOW}
mercuryData = {"dist": 69.022 * million * km, "radius": 2_439.7 * km, "mass": 3.285 * (10 ** 23), "speed": 520_000, "colour": MERCURY}
venusData = {"dist": 108.87 * million * km, "radius": 6_051.8 * km, "mass": 4.867 * (10 ** 24), "speed": 430_000, "colour": VENUS}
earthData = {"dist": 148.41 * million * km, "radius": 6_371 * km, "mass": 5.97219 * (10 ** 24), "speed": 380_000, "colour": EARTH}
marsData  = {"dist": 239.24 * million * km, "radius": 3_389.5 * km, "mass": 6.39 * (10 ** 23), "speed": 300_000, "colour": MARS}
jupiterData = {"dist": 778.5 * million * km, "radius": 69_911 * km, "mass": 1.898 * (10 ** 27), "speed": 340_000, "colour": JUPITER}
#saturnData
#uranusData
#neptuneData

# getting position of the sun
# this being the centre of the screen
sunPos = (WIDTH//2 * 1_000_000_000, HEIGHT//2 * 1_000_000_000)

sun = bodyGen(sunData, "Sun", sunPos, stat = True)
earth = bodyGen(earthData, "Earth", sunPos, drawTrail = True)
mars = bodyGen(marsData, "Mars", sunPos, drawTrail = True)
mercury = bodyGen(mercuryData, "Mercury", sunPos, drawTrail = True)
venus = bodyGen(venusData, "Venus", sunPos, drawTrail = True)

planets = [sun, earth, mars]


while True:
    # termination when cross in pressed on pygame window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    
    win.fill(BLACK)
    delta = clock.tick(FPS) /1000
    for planet in planets:
        planet.updateVel([sun])
    for planet in planets:
        planet.updatePos(delta)
        planet.show()

    pygame.display.update()
    pygame.display.update()

