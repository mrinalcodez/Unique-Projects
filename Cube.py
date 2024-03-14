import pygame                           # importing all the modules
import math
import sys
import numpy as np
import os


os.environ["SDL_VIDEO_CENTERED_POS"] = '1'

pygame.init()
                                                              # initialising all the necessary variables and the screen
A, B, C = 0.0, 0.0, 0.0

screen = pygame.display.set_mode((1200, 600))

width, height = 80, 44

K2 = 60

K1 = 5

font = pygame.font.SysFont("Arial", 18)

def calculateX(i, j, k):
    return j*math.sin(A)*math.sin(B)*math.cos(C) - k*math.cos(A)*math.sin(B)*math.cos(C) + j*math.cos(A)*math.sin(C) + k*math.sin(A)*math.sin(C) + i*math.cos(B)*math.cos(C)
                                                                                      # calculating the 3d coordinates using the matrix multiplication
def calculateY(i, j, k):
    return j*math.cos(A)*math.cos(C) + k*math.sin(A)*math.cos(C) - j*math.sin(A)*math.sin(B)*math.sin(C) + k*math.cos(A)*math.sin(B)*math.sin(C) - i*math.cos(B)*math.sin(C)

def calculateZ(i, j, k):
    return k*math.cos(A)*math.cos(B) - j*math.sin(A)*math.cos(B) + i*math.sin(B)

def calculatesurface(cubeX, cubeY, cubeZ):
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + K2
    
    ooz = 1/z
    
    xp = int(width/2 + K1*ooz*x)                                                   # calculating the projected x and y coordinates by taking K1*x/z and K1*y/z
    yp = int(height/2 + K1*ooz*y)
    
    if ooz > zBuffer[xp][yp] and 0 <= xp < width and 0 <= yp < height:               # calculating the projection of light based on luminance index
        zBuffer[xp][yp] = ooz
        buffer[xp][yp] = '!@#*.+'[]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    x, y = 0, 0
    zBuffer = np.zeros((width, height), dtype=float)
    buffer = np.full((width, height), ' ', dtype=str)
    
    cubeX = -29
    while cubeX < 30:
        cubeY = -29
        while cubeY < 30:                                                                  # initialsing the output array and z buffer array for depth of image amd also taking the coordinates of the sides
            calculatesurface(cubeX, cubeY, -30)
            cubeY += 0.6
        cubeX += 0.6
      
    for i in range(height):
        for j in range(width):
            x += 15
            if buffer[j, i] == '+':                                                            
                text = font.render(buffer[j, i], False, 'white')                           # rendering the output array on the screen and printing it
                screen.blit(text, (x, y))  
        y += 15
        x = 0  


    A += 0.05
    B += 0.05
    C += 0.05
    
    pygame.display.flip()                              #Always remember to update the screen
    
    screen.fill('black')
