from __future__ import annotations
import random
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Alien(Sprite):
    """Una clase para representar un solo alien en la flota.

    Parameters
    ----------
    Sprite : _type_
        _description_
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Inicializa el alien y establece su posición inicial

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carga la imagen del alien y configura su atributo rect.
        # Cargamos una nave aleatoriamente
        nave_alien = random.choice(list(self.settings.alien_path.iterdir()))
        self.image = pygame.image.load(nave_alien)
        self.rect = self.image.get_rect()

        # Inicia in nuevo alien cerca de la parte superior izquierda
        # de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Guarda la posición horzontal exacta del alien.
        self.x = self.rect.x
