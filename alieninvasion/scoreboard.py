from __future__ import annotations
from typing import TYPE_CHECKING

import pygame.font

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class Scoreboard:
    """Una clase para dar información de la puntuación
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Inicializa los atributos de puntuación

        Parameters
        ----------
        ai_game : AlienInvasion
            _description_
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Configuración de fuente para la información de la puntuación
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(self.settings.font, 48)

        # Prepara la imagen de la puntuación inicial y high score
        self.prep_score()
        self.prep_high_score()

    def prep_high_score(self) -> None:
        """Convierte la puntuación más alta en una imagen renderizada
        """
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True,
            self.text_color
            )

        # Centra la puntuación en la parte superior de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_score(self) -> None:
        """Convierte la puntuación en una imagen renderizada
        """
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True,
            self.text_color
            )
        # Muestra la puntuación en la parte superior derecha
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def check_high_score(self) -> None:
        """Comprueba si hay una nueva puntuación más alta"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self) -> None:
        """Dibuja la puntuación en la pantalla
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
