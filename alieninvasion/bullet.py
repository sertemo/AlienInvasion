from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """Una clase para gestionar las balas disparadas
    dessde la nave

    Parameters
    ----------
    Sprite : _type_
        _description_
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Crea un objeto para la bala en la posición actual
        de la nave

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Crea un rectangulo para la bala en (0, 0) y luego establece la
        # posición correcta
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = self.rect.y

    def update(self) -> None:
        """Mueve la bala hacia arriba por la pantalla"""
        # Actualiza la posición exacta de la bala
        self.y -= self.settings.bullet_speed
        # Actualiza la posición del rectangulo
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """Dibuja la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)
