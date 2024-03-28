import sys

import pygame

from settings import Settings


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
            (self.settings.screen_width, self.settings.scree_height))

    def run_game(self) -> None:
        """Inicia el bucle principal del juego
        """
        while True:
            # Busca eventos de teclado y ratón
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # Redibuja la pantalla en cada paso por el bucle
                self.screen.fill(self.settings.bg_color)

            # Hace visible la ultima pantalla dibujada
            pygame.display.flip()
            self.clock.tick(self.settings.fps)


if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()
