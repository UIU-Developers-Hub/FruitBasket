import math
import pygame
from typing import Tuple, List
import random


class DropAbleSpriteBaseClass(pygame.sprite.Sprite):
    """
    DropAbleSpriteBaseClass represents a sprite that falls under gravity and exhibits a swinging effect during its fall.

    Attributes:
    - __DEFAULT_GRAVITY (int): Class attribute representing the default gravity value. The gravity affects the downward acceleration of the sprite during its fall.
    - singleSrcImgSprite (bool): Boolean attribute indicating whether the sprite has a single source image.
    - windowWH (Tuple[int]): Tuple representing the dimensions (width, height) of the game window.
    - animate (bool): Boolean indicating whether animation is enabled for the sprite.
    - scaleable (bool): Boolean indicating whether the sprite is scalable.
    - scaleValue (float): Float representing the scale factor of the sprite.
    - gravity (int): Integer representing the gravitational force applied to the sprite.
    - acc (float): Float representing the accumulated acceleration of the sprite.
    - oscillationDirection (int): Integer representing the direction of oscillation (-1 for left, 1 for right).
    - rotation_angle (float): Float representing the accumulated rotation angle during oscillation.
    - rotation_speed (float): Float representing the speed at which the rotation angle changes.
    - spriteGenaratePos (Tuple[int]): Tuple representing the initial position of the sprite.

    Methods:
    - __init__: Initializes the DropAbleSpriteBaseClass instance.
    - __apply_physics: Applies physics simulation to the sprite based on gravity and time.
    - __fall_rotation: Applies a swinging effect to the sprite during its fall.
    - __handle_single_src_image: Handles loading and scaling of a single source image for the sprite.
    - __handle_multi_src_images: Handles loading and scaling of multiple source images for the sprite.
    - load_src_images: Chooses between handling a single or multiple source images based on input.
    - make_images: Initializes the sprite's image, rect, and position vector.
    - animate: Placeholder method for sprite animation (to be implemented).
    - update: Updates the sprite's state based on time and physics, handles animation, and checks if the sprite has fallen out of the window.

    """

    __DEFAULT_GRAVITY: int = 377

    def __init__(
        self,
        imagesSrc: Tuple[str],
        groups : "pygame.sprite.Group",
        windowWH: Tuple[int],
        scaleable: bool,
        scaleValue: float,
        animate: bool,
        randomFactor: Tuple[int] = None,
    ) -> None:
        """
        Initializes a DropAbleSpriteBaseClass instance.

        Args:
        - imagesSrc (Tuple[str]): Tuple containing the file paths of sprite images.
        - groups (pygame.sprite.Group): Pygame sprite groups to which the sprite belongs.
        - windowWH (Tuple[int]): Tuple representing the dimensions (width, height) of the game window.
        - scaleable (bool): Boolean indicating whether the sprite is scalable.
        - scaleValue (float): Float representing the scale factor of the sprite.
        - animate (bool): Boolean indicating whether animation is enabled for the sprite.
        - randomFactor (Tuple[int], optional): Tuple representing the random factors for sprite generation. Defaults to None.
        """
        super().__init__(groups)

        self.singleSrcImgSprite: bool = False
        self.windowWH: Tuple[int] = windowWH
        self.animate: bool = animate
        self.scaleable: bool = scaleable
        self.scaleValue: float = scaleValue
        self.gravity: int = DropAbleSpriteBaseClass.__DEFAULT_GRAVITY
        self.acc: float = 0.0
        self.oscillationDirection : int = random.choice([1, -1])
        self.rotation_angle: float = 0.0
        self.rotation_speed: float = random.uniform(100.0, 500.0)

        if randomFactor:
            self.spriteGenaratePos: Tuple[int] = (
                random.randint(randomFactor[0], randomFactor[1]),
                -1 * random.randint(100, 150),
            )
        else:
            self.spriteGenaratePos: Tuple[int] = (
                random.randint(0, windowWH[0]),
                -1 * random.randint(100, 150),
            )

        self.load_src_images(imagesSrc, scaleable, scaleValue)
        self.make_images()
        self.__fall_rotation()

    def __apply_physics(self, dt: float) -> None:
        """
        Applies physics simulation to the sprite based on gravity and time.

        Args:
        - dt (float): Time passed since the last frame.
        """
        self.acc += self.gravity * dt
        self.posVector.y += self.acc * dt
        self.rect.y = round(self.posVector.y)

    def __fall_rotation(self, amplitude: float = 10.0) -> None:
        """
        Applies a swinging effect to the sprite during its fall.

        Args:
        - amplitude (float, optional): Amplitude of the swinging effect. Defaults to 10.0.
        """
        self.rotation_angle : float= self.oscillationDirection * self.rotation_speed
        rotated_image : "pygame.surface.Surface" = pygame.transform.rotate(self.srcImages[0], self.rotation_angle)
        self.image : "pygame.surface.Surface" = rotated_image

    def __handle_single_src_image(self, imagesSrc: Tuple[str], scaleable: bool, scaleValue: float) -> None:
        """
        Handles loading and scaling of a single source image for the sprite.

        Args:
        - imagesSrc (Tuple[str]): Tuple containing the file paths of sprite images.
        - scaleable (bool): Boolean indicating whether the sprite is scalable.
        - scaleValue (float): Float representing the scale factor of the sprite.
        """
        self.singleSrcImgSprite = True
        self.srcImages : List["pygame.surface.Surface"] = [pygame.image.load(imagesSrc[0]).convert_alpha()]

        if scaleable:
            self.srcImages[0] = pygame.transform.scale(
                self.srcImages[0], pygame.math.Vector2(self.srcImg.get_size()) * scaleValue
            )

    def __handle_multi_src_images(self, imagesSrc: Tuple[str], scaleable: bool, scaleValue: float) -> None:
        """
        Handles loading and scaling of multiple source images for the sprite.

        Args:
        - imagesSrc (Tuple[str]): Tuple containing the file paths of sprite images.
        - scaleable (bool): Boolean indicating whether the sprite is scalable.
        - scaleValue (float): Float representing the scale factor of the sprite.
        """
        self.srcImages : List["pygame.surface.Surface"] = []

        for srcImg in self.srcImages:
            img : "pygame.surface.Surface" = pygame.image.load(srcImg).convert_alpha()
            if scaleable:
                img = pygame.transform.scale(
                    img, pygame.math.Vector2(img.get_size()) * scaleValue
                )
            self.srcImages.append(img)

    def load_src_images(self, imagesSrc: Tuple[str], scaleable: bool, scaleValue: float) -> None:
        """
        Chooses between handling a single or multiple source images based on input.

        Args:
        - imagesSrc (Tuple[str]): Tuple containing the file paths of sprite images.
        - scaleable (bool): Boolean indicating whether the sprite is scalable.
        - scaleValue (float): Float representing the scale factor of the sprite.
        """
        if len(imagesSrc) == 1:
            self.__handle_single_src_image(imagesSrc, scaleable, scaleValue)
        else:
            self.__handle_multi_src_images(imagesSrc, scaleable, scaleValue)

    def make_images(self) -> None:
        """
        Initializes the sprite's image, rect, and position vector.
        """
        self.image : "pygame.surface.Surface" = self.srcImages[0]
        self.rect : "pygame.Rect" = self.image.get_rect(topleft=self.spriteGenaratePos)
        self.posVector : "pygame.math.Vector2" = pygame.math.Vector2(self.rect.topleft)

    def animate(self, dt: float) -> None:
        """
        Placeholder method for sprite animation (to be implemented).

        Args:
        - dt (float): Time passed since the last frame.
        """
        # TO-DO
        pass

    def update(self, dt: float) -> None:
        """
        Updates the sprite's state based on time and physics, handles animation, and checks if the sprite has fallen out of the window.

        Args:
        - dt (float): Time passed since the last frame.
        """
        self.__apply_physics(dt)
        if self.animate:
            self.animate(dt)
        if self.posVector.y > self.windowWH[1] + 100:
            self.kill()
