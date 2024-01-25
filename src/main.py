import sys
import pygame
from typing import List

from gameObjects import StaticBackgroundImageBaseClass

# helper variables
active : bool = True
point : int = 0
windowWidth, windowHeight = windowConfig = (680, 980)
fruitsAssets : List[str] = None
bugAssets : List[str] = None

# initializing pygame must do
pygame.init()

# Pygame variables/objects
window = pygame.display
window.set_mode(windowConfig)
mainSurface = window.get_surface()
font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)

# Game objects and other variables
backGround : StaticBackgroundImageBaseClass = StaticBackgroundImageBaseClass("assets/bg/bg.jpg", (0, 0))

# Game Loop
while active:
    mainSurface.fill("Black")
    mainSurface.blit(backGround.get_render_object((windowHeight + 1) / backGround.image.get_height()), backGround.get_render_object_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False


    window.update()

# Game exit logic
pygame.quit()
sys.exit()