from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Explosion(Sprite):
    """Clase Sprite para mostrar una explosión
    cuando una nave alienígena explota

    Parameters
    ----------
    Sprite : _type_
        _description_
    """
    def __init__(
            self, center: tuple[int, int] # posición del alien
            ) -> None:
        super().__init__()
        self.images = [
            pygame.image.load('explosion1.png').convert_alpha(),
            pygame.image.load('explosion2.png').convert_alpha(),
            pygame.image.load('explosion3.png').convert_alpha(),
            pygame.image.load('explosion4.png').convert_alpha(),
            pygame.image.load('explosion5.png').convert_alpha()
        ]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 3  # Controla la velocidad de la animación

    def update(self):
        self.current_frame += 1
        if self.current_frame >= len(self.images) * self.frame_rate:
            self.kill()  # Termina la animación y elimina el sprite
        else:
            # Actualiza la imagen sólo en ciertos frames para ralentizar la animación
            self.image = self.images[self.current_frame // self.frame_rate]