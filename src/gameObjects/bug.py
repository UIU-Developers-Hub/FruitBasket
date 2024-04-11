from typing import Tuple
from pygame.sprite import Group
from . import DropAbleSpriteBaseClass

class Bug(DropAbleSpriteBaseClass):
    def __init__(self, imagesSrc: Tuple[str], groups: Group, windowWH: Tuple[int], scaleable: bool, scaleValue: float, animate: bool, damage: int, gravity: int = None, randomFactor: Tuple[int] = None) -> None:
        """
        Constructor for Bug class.

        Args:
            imagesSrc (Tuple[str]): Tuple of image file paths for the bug.
            groups (Group): Sprite groups to add the bug to.
            windowWH (Tuple[int]): Window width and height.
            scaleable (bool): Flag indicating if the bug is scalable.
            scaleValue (float): Scale value for the bug.
            animate (bool): Flag indicating if the bug should be animated.
            damage (int): Damage value inflicted by the bug.
            gravity (int, optional): Gravity value for the bug. Defaults to None.
            randomFactor (Tuple[int], optional): Tuple representing a range of random factors. Defaults to None.
        """
        super().__init__(imagesSrc, groups, windowWH, scaleable, scaleValue, animate, randomFactor)
        self.damage: int = damage
        
        if gravity:
            self.gravity = gravity
