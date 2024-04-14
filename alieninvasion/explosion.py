from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font
from pygame.sprite import Sprite

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Explosion(Sprite):
    """Clase para generar una explosión al reventar
    una nave alienígena

    Parameters
    ----------
    Sprite : _type_
        _description_
    """
    def __init__(
            self,
            ai_game: AlienInvasion,
            center: tuple[int, int] # posición del alien
            ) -> None:
        """inicializa las imágenes de la explosión

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        center : tuple[int, int]
            _description_
        """
        super().__init__()
        self.settings = ai_game.settings
        self.images = [
            pygame.image.load(self.settings.explosion_path / 'ex1.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex2.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex3.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex4.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex5.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex6.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex7.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex8.png').convert_alpha(),
            pygame.image.load(self.settings.explosion_path / 'ex9.png').convert_alpha()
        ]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 2  # Controla la velocidad de la animación

    def update(self):
        self.current_frame += 1
        if self.current_frame >= len(self.images) * self.frame_rate:
            self.kill()  # Termina la animación y elimina el sprite
        else:
            # Actualiza la imagen sólo en ciertos frames para ralentizar la animación
            self.image = self.images[self.current_frame // self.frame_rate]