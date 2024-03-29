import sys

import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Clase geenral para gestionar los recursos y el comportamiento
    del juego
    """

    def __init__(self) -> None:
        """Inicializa el juego y crea recursos
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        # Color de fondo
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)

    def run_game(self) -> None:
        """Inicia el bucle principal del juego
        """
        while True:
            # Busca eventos de teclado y ratón
            self._check_events()
            # Actualiza la posición de la nave
            self.ship.update()
            # Actualizamos la pantalla
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self) -> None:
        """Responde a pulsaciones de teclas y eventos de ratón
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Mueve la nave a la derecha
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    # Mueve la nave a la derecha
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self) -> None:
        """Actualiza las imágenes en la pantalla y cambia
        a la pantalla nueva
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Hace visible la ultima pantalla dibujada
        pygame.display.flip()


if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()
