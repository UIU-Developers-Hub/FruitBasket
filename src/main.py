import sys
import time
import pygame
import random
from pathlib import Path
from typing import List, Dict

from utility import *
from gameObjects import StaticBackgroundImageBaseClass, Fruit, Bug

# helper variables
active : bool = True
point : int = 0
windowWidth, windowHeight = windowConfig

fruitAssetsFolderObj = Path(folderPaths["fruit"])
fruitsAssets : List[str] = [str(file) for file in fruitAssetsFolderObj.iterdir() if file.is_file()]
fruitPoint : Dict[str, int] = {key: key.split("//")[-1].split(".")[0][-1] for key in fruitsAssets}

bugAssetsFolderObj = Path(folderPaths["bug"])
bugAssets : List[str] = [str(file) for file in bugAssetsFolderObj.iterdir() if file.is_file()]
bugDamage : Dict[str, int] = {key: key.split("//")[-1].split(".")[0][-1] for key in bugAssets}

# initializing pygame must do
pygame.init()

# Pygame variables/objects
window = pygame.display
window.set_mode(windowConfig)
mainSurface = window.get_surface()
font = pygame.font.Font(filePaths["font"], fontSize)

# Game objects and other variables
backGround : StaticBackgroundImageBaseClass = StaticBackgroundImageBaseClass(filePaths["bg"], (0, 0))
fruitGroup = pygame.sprite.Group()
bugGroup = pygame.sprite.Group()

# Game Loop
lastTime = time.time()
while active:
    dt = time.time() - lastTime
    lastTime = time.time()

    mainSurface.fill("Black")
    mainSurface.blit(backGround.get_render_object((windowHeight + 1) / backGround.image.get_height()), backGround.get_render_object_pos())
    
    if random.randint(0, 100) < 3 and len(fruitGroup) < 4:
        Fruit(
            (random.choice(fruitsAssets),),
            fruitGroup,
            windowConfig,
            True,
            .9,
            False,
            10,
            random.choice(
                (
                    (30, 50),
                    (100, 200),
                    (250, 350),
                    (180, 380)
                )
            )
        )

    if random.randint(0, 100) < 1 and len(bugGroup) < 2:
        Bug(
            (random.choice(bugAssets),),
            bugGroup,
            windowConfig,
            True,
            .5,
            False,
            10,
            random.choice(
                (
                    (50, 100),
                    (120, 160),
                    (200, 280)
                )
            )
        )

    for fruit in fruitGroup:
        fruit.update(dt)

    for bug in bugGroup:
        bug.update(dt)

    fruitGroup.draw(mainSurface)
    bugGroup.draw(mainSurface)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    window.update()

# Game exit logic
pygame.quit()
sys.exit()