from __future__ import annotations
from typing import TYPE_CHECKING

from icecream import ic

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class GameStats:
    """Sigue las estadísticas de Alien Invasion"""

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Inicializa las estadísticas

        Parameters
        ----------
        ai_game : _type_
            _description_
        """
        self.settings = ai_game.settings
        self.reset_stats()  # Para partida nueva

        # Cargamos Puntuación record del archivo en db
        self.high_score = int(self.settings.high_score_path.read_text())

    def save_highscore(self) -> None:
        """Guarda en archivo el highscore"""
        ic(self.high_score, type(self.high_score))
        high_score_str = str(self.high_score)
        self.settings.high_score_path.write_text(high_score_str)

    def reset_stats(self) -> None:
        """Inicializa las estadísticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.bonus_stats = {"extra_speed": 0, "extra_bullets": 0, "extra_life": 0}
