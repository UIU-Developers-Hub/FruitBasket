import sys
import time
import pygame
import random
from pathlib import Path
from typing import List, Dict

from utility import *
from gameObjects import StaticBackgroundImageBaseClass, Fruit, Bug, Busket


class Game:
    NAME = "Fruit Busket"
    STATE = (
        "PlayState",
        "MenuState",
        "PauseState"
    )
    
    def __init__(self, windowConfig) -> None:
        pygame.init()
        
        self.windowConfig = windowConfig
        self.windowWidth, self.windowHeight = windowConfig
        
        self.state = Game.STATE[1]
        self.active = False
        self.clock = pygame.time.Clock()
        self.maxFPS = 60
        
        self.point : int = 0
        self.lvl : int = self.__set_level()
        
        self.__config_window()
        self.__setup_font()
        self.__load_fruit_assets()
        self.__load_bug_assets()
        self.__setup_game_objects()
        
    def __config_window(self) -> None:
        self.window = pygame.display
        self.window.set_mode(self.windowConfig)
        self.window.set_caption(Game.NAME)
        self.mainSurface = self.window.get_surface()
        
    def __setup_font(self) -> None:
        self.font = pygame.font.Font(filePaths["font"], fontSize)
        self.font.bold = True
    
    def __load_fruit_assets(self) -> None:
        fruitAssetsFolderObj = Path(folderPaths["fruit"])
        self.fruitsAssets : List[str] = [str(file) for file in fruitAssetsFolderObj.iterdir() if file.is_file()]
        self.fruitPoint : Dict[str, int] = {key: key.split("//")[-1].split(".")[0][-1] for key in self.fruitsAssets}
    
    def __load_bug_assets(self) -> None:
        bugAssetsFolderObj = Path(folderPaths["bug"])
        self.bugAssets : List[str] = [str(file) for file in bugAssetsFolderObj.iterdir() if file.is_file()]
        self.bugDamage : Dict[str, int] = {key: key.split("//")[-1].split(".")[0][-1] for key in self.bugAssets}
    
    def __setup_game_objects(self):
        self.backGround : StaticBackgroundImageBaseClass = StaticBackgroundImageBaseClass(filePaths["bg"], (0, 0))
        self.fruitGroup = pygame.sprite.Group()
        self.bugGroup = pygame.sprite.Group()
        self.player = Busket(filePaths["player"], 100)
    
    def __set_level(self) -> int:
        if self.point in range(0, 201):
            return 1
        if self.point in range(201, 601):
            return 2
        if self.point in range(401, 1001):
            return 3
        if self.point in range(1001, 1801):
            return 4
        
        return 5
        
    def __game_loop(self):
        lastTime = time.time()
        while self.active:
            self.point += 1
            self.lvl = self.__set_level()
            dt = (time.time() - lastTime)
            lastTime = time.time()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
            
            self.mainSurface.fill("Black")
            self.mainSurface.blit(
                self.backGround.get_render_object(
                    (self.windowHeight + 1) / self.backGround.image.get_height()
                ),
                self.backGround.get_render_object_pos()
            )
            
            if random.randint(0, 100) < 3 and len(self.fruitGroup) < levelWiseParameters[self.lvl]["fruitSpwanLimit"]:
                Fruit(
                    (random.choice(self.fruitsAssets),),
                    self.fruitGroup, self.windowConfig,
                    True, .9, False, 10, levelWiseParameters[self.lvl]["fruitG"],
                    random.choice(
                        (
                            (30, 50),
                            (100, 200),
                            (250, 350),
                            (180, 380)
                        )
                    )
                )

            if random.randint(0, 100) < 1 and len(self.bugGroup) < levelWiseParameters[self.lvl]["bugSpwanLimit"]:
                Bug(
                    (random.choice(self.bugAssets),),
                    self.bugGroup, self.windowConfig,
                    True, .5, False, 10, levelWiseParameters[self.lvl]["bugG"],
                    random.choice(
                        (
                            (50, 100),
                            (120, 160),
                            (200, 280)
                        )
                    )
                )

            for fruit in self.fruitGroup:
                fruit.update(dt)

            for bug in self.bugGroup:
                bug.update(dt)

            self.fruitGroup.draw(self.mainSurface)
            self.bugGroup.draw(self.mainSurface)
            
            self.mainSurface.blit(
                self.font.render(f"P: {self.point}", False, "white"),
                (5, 5, 20, 20)
            )
            self.mainSurface.blit(
                self.font.render(f"L: {self.player.live}", False, "white"),
                (self.windowWidth-100, 5, 20, 20)
            )
            self.mainSurface.blit(
                self.font.render(f"LVL: {self.lvl}", False, "white"),
                (self.windowWidth/2-50, 5, 20, 20)
            )
            self.mainSurface.blit(
                self.font.render("_"*int((self.windowWidth/15)), False, "white"),
                (0, 12, self.windowWidth, 20)
            )

            self.window.update()
            self.clock.tick(self.maxFPS)
        
    def run(self):
        self.active = True
        self.__game_loop()
        self.__clean_up()
    
    def __clean_up(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game(windowConfig).run()