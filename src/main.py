import sys
import time
import pygame
import random
from pathlib import Path
from typing import List, Dict

from utility import *  # Importing utility functions and constants
from gameObjects import StaticBackgroundImageBaseClass, Fruit, Bug, Busket  # Importing game object classes

class Game:
    """
    Main class for the Fruit Busket game.
    """

    NAME = "Fruit Busket"
    MAXSOCRE = 0
    STATE = (
        "PlayState",
        "MenuState",
        "PauseState",
        "GameOver"
    )

    def __init__(self, windowConfig) -> None:
        """
        Initializes the game.
        
        Args:
            windowConfig: A tuple containing the window width and height.
        """
        pygame.init()

        self.windowConfig = windowConfig
        self.windowWidth, self.windowHeight = windowConfig

        # Initial game state
        self.state = Game.STATE[1]  # Start with MenuState
        self.active = False  # Game active flag
        self.clock = pygame.time.Clock()  # Pygame clock object
        self.maxFPS = 60  # Maximum frames per second

        # Player score and level
        self.point: int = 0
        self.lvl: int = self.__set_level()

        # Configure window and initialize fonts and game objects
        self.__config_window()
        self.__setup_font()
        self.__load_fruit_assets()
        self.__load_bug_assets()
        self.__setup_game_objects()

    def __config_window(self) -> None:
        """
        Configures the game window.
        """
        self.window = pygame.display
        self.window.set_mode(self.windowConfig)
        self.window.set_caption(Game.NAME)
        self.mainSurface = self.window.get_surface()

    def __setup_font(self) -> None:
        """
        Initializes fonts for the game.
        """
        self.font = pygame.font.Font(filePaths["font"], fontSize)
        self.font.bold = True
        self.menuFont = pygame.font.Font(filePaths["font"], fontSize - 10)
        self.menuFont.bold = False

    def __load_fruit_assets(self) -> None:
        """
        Loads fruit assets.
        """
        fruitAssetsFolderObj = Path(folderPaths["fruit"])
        self.fruitsAssets: List[str] = [str(file) for file in fruitAssetsFolderObj.iterdir() if file.is_file()]
        self.fruitPoint: Dict[str, int] = {key: int(key.split("//")[-1].split(".")[0][-1]) + 10 for key in
                                           self.fruitsAssets}

    def __load_bug_assets(self) -> None:
        """
        Loads bug assets.
        """
        bugAssetsFolderObj = Path(folderPaths["bug"])
        self.bugAssets: List[str] = [str(file) for file in bugAssetsFolderObj.iterdir() if file.is_file()]
        self.bugDamage: Dict[str, int] = {key: int(key.split("//")[-1].split(".")[0][-1]) + 11 for key in
                                          self.bugAssets}

    def __setup_game_objects(self):
        """
        Sets up game objects.
        """
        self.backGround: StaticBackgroundImageBaseClass = StaticBackgroundImageBaseClass(filePaths["bg"], (0, 0))
        self.fruitGroup = pygame.sprite.Group()
        self.bugGroup = pygame.sprite.Group()
        self.player = Busket(filePaths["player"], 100, self.windowHeight - 150, [-100, self.windowWidth],
                             scaleFactor=0.25)

    def __set_level(self) -> int:
        """
        Determines the game level based on the player's score.

        Returns:
            The game level.
        """
        if self.point in range(0, 201):
            return 1
        if self.point in range(201, 601):
            return 2
        if self.point in range(401, 1001):
            return 3
        if self.point in range(1001, 1801):
            return 4

        return 5

    def __game_logic(self, dt: float) -> None:
        """
        Handles game logic.

        Args:
            dt: Time elapsed since the last frame.
        """
        # Spawning fruits
        if random.randint(0, 100) < 3 and len(self.fruitGroup) < levelWiseParameters[self.lvl]["fruitSpwanLimit"]:
            selectedFruit = random.choice(self.fruitsAssets)
            Fruit(
                (selectedFruit,),
                self.fruitGroup, self.windowConfig,
                True, .9, False, self.fruitPoint[selectedFruit], levelWiseParameters[self.lvl]["fruitG"],
                random.choice(
                    (
                        (30, 50),
                        (100, 200),
                        (250, 350),
                        (180, 380)
                    )
                )
            )

        # Spawning bugs
        if random.randint(0, 100) < 1 and len(self.bugGroup) < levelWiseParameters[self.lvl]["bugSpwanLimit"]:
            selectedBug = random.choice(self.bugAssets)
            Bug(
                (selectedBug,),
                self.bugGroup, self.windowConfig,
                True, .5, False, self.bugDamage[selectedBug], levelWiseParameters[self.lvl]["bugG"],
                random.choice(
                    (
                        (50, 100),
                        (120, 160),
                        (200, 280)
                    )
                )
            )

        # Update fruits
        for fruit in self.fruitGroup:
            fruit.update(dt)
            if self.player.collision_occured(fruit):
                self.point += fruit.point
                fruit.kill()

        # Update bugs
        for bug in self.bugGroup:
            bug.update(dt)
            if self.player.collision_occured(bug):
                self.player.live -= bug.damage
                bug.kill()

        # Draw game elements on the screen
        self.fruitGroup.draw(self.mainSurface)
        self.bugGroup.draw(self.mainSurface)

        # Display player score, lives, and level
        self.mainSurface.blit(
            self.font.render(f"P: {self.point}", False, "white"),
            (5, 5, 20, 20)
        )
        self.mainSurface.blit(
            self.font.render(f"L: {self.player.live if self.player.live > 0 else 0}", False, "white"),
            (self.windowWidth - 100, 5, 20, 20)
        )
        self.mainSurface.blit(
            self.font.render(f"LVL: {self.lvl if self.lvl != 5 else ' MAX'}", False, "white"),
            (self.windowWidth / 2 - 50, 5, 20, 20)
        )
        self.mainSurface.blit(
            self.font.render("_" * int((self.windowWidth / 15)), False, "white"),
            (0, 12, self.windowWidth, 20)
        )

        # Draw player object
        self.player.draw_on(self.mainSurface)

        # Check for game over condition
        if self.player.live <= 0:
            self.state = Game.STATE[3]

    def __render_menu(self) -> None:
        """
        Renders the game menu.
        """
        if self.state == Game.STATE[1]:
            self.mainSurface.blit(self.menuFont.render("Press Enter To Play !", False, "white"),
                                  (110, 220, self.windowWidth, 80))
            self.mainSurface.blit(self.menuFont.render(f"MAX SCORE : {Game.MAXSOCRE}", False, "white"),
                                  (150, 260, self.windowWidth, 80))
        elif self.state == Game.STATE[3]:
            self.mainSurface.blit(
                self.menuFont.render(f"YOUR SCORE: {self.point}", False, "white"),
                (self.windowWidth / 2 - 95, self.windowHeight / 2 - 10, 200, 200)
            )
            self.mainSurface.blit(
                self.menuFont.render("GAME OVER :(", False, "white"),
                (self.windowWidth / 2 - 70, self.windowHeight / 2 - 40, 200, 200)
            )
            return
        else:
            self.mainSurface.blit(self.menuFont.render("PAUSE", False, "white"), (200, 220, self.windowWidth, 80))

        # Render instructions
        self.mainSurface.blit(self.menuFont.render(f"Use Space key To Pause", False, "white"),
                              (100, 450, self.windowWidth, 80))
        self.mainSurface.blit(self.menuFont.render("Use Left and Right key to move.", False, "white"),
                              (60, 500, self.windowWidth, 80))

    def __reset(self):
        """
        Resets the game state.
        """
        Game.MAXSOCRE = max(self.point, Game.MAXSOCRE)
        self.point = 0
        self.player.live = 100
        self.lvl = 1
        [fruit.kill() for fruit in self.fruitGroup]
        [bug.kill() for bug in self.bugGroup]

    def __game_loop(self):
        """
        Main game loop.
        """
        lastTime = time.time()
        while self.active:
            self.lvl = self.__set_level()
            dt = (time.time() - lastTime)
            lastTime = time.time()

            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.state == Game.STATE[0]:
                        self.player.move(-1 * 2 * levelWiseParameters[self.lvl]["playerSpd"])
                    elif event.key == pygame.K_RIGHT and self.state == Game.STATE[0]:
                        self.player.move(2 * levelWiseParameters[self.lvl]["playerSpd"])
                    elif event.key == pygame.K_RETURN:
                        if self.state == Game.STATE[1]:
                            self.state = Game.STATE[0]
                        elif self.state == Game.STATE[3]:
                            self.__reset()
                            self.state = Game.STATE[1]
                    elif event.key == pygame.K_SPACE:
                        if self.state == Game.STATE[0]:
                            self.state = Game.STATE[2]
                        elif self.state == Game.STATE[2]:
                            self.state = Game.STATE[0]
                        elif self.state == Game.STATE[3]:
                            self.__reset()
                            self.state = Game.STATE[1]

            # Clear the screen
            self.mainSurface.fill("Black")

            # Draw background
            self.mainSurface.blit(
                self.backGround.get_render_object(
                    (self.windowHeight + 1) / self.backGround.image.get_height()
                ),
                self.backGround.get_render_object_pos()
            )

            # Update game logic or render menu depending on the game state
            if self.state == Game.STATE[0]:
                self.__game_logic(dt)
            else:
                self.__render_menu()

            # Update the display
            self.window.update()
            self.clock.tick(self.maxFPS)

    def run(self):
        """
        Runs the game.
        """
        self.active = True
        self.__game_loop()
        self.__clean_up()

    def __clean_up(self):
        """
        Cleans up resources and quits pygame.
        """
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Initialize and run the game
    Game(windowConfig).run()
