from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Button:
    """Una clase para crear botones para el juego
    """

    def __init__(
            self,
            ai_game: AlienInvasion,
            msg: str,
            position: tuple[int ,int],
            ) -> None:
        """Inicializa los atributos del botón

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        msg : str
            _description_
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Configura las dimensiones y propiedades del botón
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font: pygame.font.Font = pygame.font.SysFont('Poppins', 48)

        # Crea el objeto rect del botón y lo centra
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Solo hay que preparar el mensaje del boton 1 vez
        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """convierte msg en una imagen renderizada y centra
        el texto en el botón

        Parameters
        ----------
        msg : str
            _description_
        """
        self.msg_image = self.font.render(
            msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        """Dibuja un boton en blanco y luego el mensaje
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
