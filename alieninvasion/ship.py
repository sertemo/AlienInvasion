from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Ship(Sprite):
    """Una clase para gestionar la nave."""

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Inicializa la nave y configura su posición
        inicial

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Carga la imagen de la nave
        self.image = pygame.image.load("alieninvasion/images/ship.png")
        self.rect = self.image.get_rect()

        # Coloca inicialmente cada nave en el centro de la parte inferior
        # de la pantalla.
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda un valor decimal para la posición horizontal exacta de la nave
        self.x = self.rect.x

        # Creamos flags de movimiento continuo
        self.moving_right = False
        self.moving_left = False

    def update(self) -> None:
        """Actualiza la posición de la nave en función
        de la flag
        """
        # Actualiza el valor x de la nave, no el rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Actualiza el objeto rect de self.x
        self.rect.x = self.x

    def center_ship(self) -> None:
        """Centra la nave en la pantalla."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = self.rect.x

    def blitme(self) -> None:
        """Dibuja la nave en la ubicación actual"""
        self.screen.blit(self.image, self.rect)
