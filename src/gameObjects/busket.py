import pygame

class Busket(pygame.sprite.Sprite):
    def __init__(self, image: str, live: int, posY: int, movementRange: tuple, scaleFactor: float = None) -> None:
        """
        Constructor for Busket class.

        Args:
            image (str): Path to the image file for the busket.
            live (int): Initial live value of the busket.
            posY (int): Initial Y position of the busket.
            movementRange (tuple): Tuple representing the range of movement for the busket.
            scaleFactor (float, optional): Scaling factor for the busket image. Defaults to None.
        """
        self.movementRange = movementRange
        self.image = pygame.image.load(image).convert_alpha()
        if scaleFactor:
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scaleFactor), int(self.image.get_height() * scaleFactor)))
        self.postRect = self.image.get_rect(topleft=(movementRange[1] // 2, posY))  # Using // for integer division
        solid_area_x = self.postRect.left + 25
        solid_area_y = self.postRect.top + self.postRect.height - 25  # Adjust the position as needed
        solid_area_width = self.postRect.width - 50
        solid_area_height = 10  # Set the height as needed
        self.solidAreaRect = pygame.Rect(solid_area_x, solid_area_y, solid_area_width, solid_area_height)
        self.live = live

    def move(self, x: int) -> None:
        """
        Move the busket horizontally.

        Args:
            x (int): Amount of horizontal movement.
        """
        newX = self.postRect[0] + x

        if newX in range(*self.movementRange):
            self.postRect[0] += x
            self.solidAreaRect[0] += x

    def draw_on(self, surface: pygame.surface.Surface) -> None:
        """
        Draw the busket on a surface.

        Args:
            surface (pygame.surface.Surface): Surface on which to draw the busket.
        """
        surface.blit(self.image, self.postRect)

    def collision_occurred(self, sprite) -> bool:
        """
        Check if a collision occurred between the busket and another sprite.

        Args:
            sprite: The sprite to check collision with.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        return self.solidAreaRect.colliderect(sprite.rect)
