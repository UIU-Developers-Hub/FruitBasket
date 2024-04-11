from typing import Tuple
from pygame.sprite import Group
from . import DropAbleSpriteBaseClass  # Assuming DropAbleSpriteBaseClass is defined in another module

class Fruit(DropAbleSpriteBaseClass):
    def __init__(self, imagesSrc: Tuple[str], groups: Group, windowWH: Tuple[int], scaleable: bool, scaleValue: float, animate: bool, point: int, gravity: int = None, randomFactor: Tuple[int] = None) -> None:
        """
        Constructor for Fruit class.

        Args:
            imagesSrc (Tuple[str]): Tuple of image file paths for the fruit.
            groups (Group): Pygame group to which the fruit sprite will be added.
            windowWH (Tuple[int]): Tuple representing the width and height of the game window.
            scaleable (bool): Flag indicating if the fruit should be scalable.
            scaleValue (float): Scaling factor for the fruit sprite.
            animate (bool): Flag indicating if the fruit should be animated.
            point (int): Point value associated with the fruit.
            gravity (int, optional): Gravity value affecting the fruit's fall speed. Defaults to None.
            randomFactor (Tuple[int], optional): Tuple representing the range of random factors affecting the fruit's behavior. Defaults to None.
        """
        super().__init__(imagesSrc, groups, windowWH, scaleable, scaleValue, animate, randomFactor)
        self.point: int = point

        if gravity:
            self.gravity = gravity
