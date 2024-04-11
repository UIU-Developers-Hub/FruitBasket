import pygame


class Busket(pygame.sprite.Sprite):
    def __init__(self, image: str, live : int) -> None:
        self.image = image
        self.rect = None
        self.live = live

    def move(self, x: int, y: int) -> None:
        pass

    def draw_on(self, surface : "pygame.surface.Surface") -> None:
        pass

    def collision_occured(self, spriteGroup) -> bool:
        pass