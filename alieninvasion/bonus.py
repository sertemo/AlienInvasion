from __future__ import annotations
import random
from typing import TYPE_CHECKING, Literal

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Bonus(Sprite):
    """Clase que representa bonmus
    de características para el jugador

    Parameters
    ----------
    Sprite : _type_
        _description_
    """

    def __init__(
        self,
        ai_game: AlienInvasion,
        type: Literal["extra_speed", "extra_bullets", "extra_life"] = "extra_speed",
    ) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.type = type

        # Cargamos la imagen del bonus en función de su tipo
        # self.image = pygame.image.load(nave_alien)

        if type == "extra_bullets":
            # Carga la imagen
            self.image = pygame.image.load("alieninvasion/images/bonus/bullet.png")
        elif type == "extra_life":
            self.image = pygame.image.load("alieninvasion/images/bonus/heart.png")
        elif type == "extra_speed":
            self.image = pygame.image.load("alieninvasion/images/bonus/arrow.png")

        # Caso genérico con cuadrado de color
        # self.image = pygame.Surface((50, 50))  # Un simple cuadrado para el ejemplo
        # self.image.fill((0, 255, 145))

        pos_x = random.randint(0, self.screen_rect.right - 50)
        self.rect = self.image.get_rect(topleft=(pos_x, 0))
        self.screen.blit(self.image, self.rect)

    def update(self) -> None:
        """Mueve el bonus hacia abajo"""
        self.rect.y += self.settings.bonus_speed
        if self.rect.top > self.screen.get_height():
            self.kill()
