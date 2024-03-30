from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Para evitar la dependencia circular. Siempre es False
    from alien_invasion import AlienInvasion


class GameStats:
    """Sigue las estadísticas de Alien Invasion
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        """Inicializa las estadísticas

        Parameters
        ----------
        ai_game : _type_
            _description_
        """
        self.settings = ai_game.settings
        self.reset_stats()  # Para partida nueva

    def reset_stats(self) -> None:
        """Inicializa las estadísticas que pueden cambiar durante el juego
        """
        self.ships_left = self.settings.ship_limit
