import sys
from typing import Any

import pygame

from bullet import Bullet
from settings import Settings
from ship import Ship
from alien import Alien


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

        # Pantalla completa
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        # Pantalla con ancho y alto definido en settings
        # self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width, self.settings.screen_height))

        self.ship = Ship(self)
        self.bullets: Any = pygame.sprite.Group()
        self.aliens: Any = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self) -> None:
        """Inicia el bucle principal del juego
        """
        while True:
            # Busca eventos de teclado y ratón
            self._check_events()
            # Actualiza la posición de la nave
            self.ship.update()
            # Actualizamos las balas
            self._update_bullets()
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
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Responde a pulsaciones de teclas

        Parameters
        ----------
        event : pygame.event.Event
            _description_
        """
        if event.key == pygame.K_RIGHT:
            # Mueve la nave a la derecha
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Mueve la nave a la derecha
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # Salimos del juego con la tecla q
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self) -> None:
        """Crea una nueva bala y la añade al grupo de balas
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Responde a liberaciones de teclas

        Parameters
        ----------
        event : pygame.event.Event
            _description_
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self) -> None:
        """Actualiza la posición de las balas y se deshace de las viejas
        """
        self.bullets.update()

        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self) -> None:
        """Crea una flota de aliens.
        """
        # Hace un alien
        alien: Alien = Alien(self)
        alien_width = alien.rect.width

        # Añade aliens hasta que no haya espacio
        # La distancia entre alienigenas es equivalente al ancho
        # de un extraterrestre
        current_x = alien_width
        while current_x < (self.screen_width - 1.5 * alien_width):
            new_alien: Alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

    def _update_screen(self) -> None:
        """Actualiza las imágenes en la pantalla y cambia
        a la pantalla nueva
        """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Hace visible la ultima pantalla dibujada
        pygame.display.flip()


if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()
