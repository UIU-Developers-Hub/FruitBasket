from typing import Tuple
from pygame.sprite import Group
from . import DropAbleSpriteBaseClass


class Bug(DropAbleSpriteBaseClass):
    def __init__(self, imagesSrc: Tuple[str], groups: Group, windowWH: Tuple[int], scaleable: bool, scaleValue: float, animate: bool, damage : int, gravity : int = None, randomFactor: Tuple[int] = None) -> None:
        super().__init__(imagesSrc, groups, windowWH, scaleable, scaleValue, animate, randomFactor)
        self.damage : int = damage
        
        if gravity:
            self.gravity = gravity