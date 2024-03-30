import sys
from time import sleep
from typing import Any

import pygame

from alien import Alien
from bullet import Bullet
from game_stats import GameStats
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

        # Pantalla completa
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        # Pantalla con ancho y alto definido en settings
        # self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width, self.settings.screen_height))

        # Crea una instancia para guardar las estadísticas del juego
        self.stats = GameStats(self)
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
            # Actualizamos la posición de los aliens
            self._update_aliens()
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

        # Busca balas que hayan dado a un alien
        # Si hay se deshace de la bala y el alien
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self) -> None:
        """Responde a las colisiones bala-alien
        """
        # Retira las balas y aliens que han chocado
        pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # Destruye las balas existentes y crea una flota nueva.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self) -> None:
        """comprueba si la flota está en un borde,
        después actualiza las posiciones de todos los aliens de la flota"""
        self._check_fleet_edges()
        self.aliens.update()

        # Busca colisiones alien-nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Busca aliens llegando al fondo de la pantalla
        self._check_aliens_bottom()

    def _ship_hit(self) -> None:
        """Responde al impacto de un alien en la nave
        """

        # Disminuye ships_left
        self.stats.ships_left -= 1

        # Se deshace de aliens y balas restantes
        self.aliens.empty()
        self.bullets.empty()

        # Crea una flota nueva y centra la nave
        self._create_fleet()
        self.ship.center_ship()

        # Pausa
        sleep(0.5)

    def _check_aliens_bottom(self) -> None:
        """Comprueba si algún alien ha llegado al fondo de la pantalla
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_height:
                # Trata esto como si la nave hubiese sido alcanzada
                self._ship_hit()
                break

    def _check_fleet_edges(self) -> None:
        """Responde adecuadamente si algún alien ha llegado al borde
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Baja toda la flota y cambia su dirección
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self) -> None:
        """Crea una flota de aliens.
        """
        # Hace un alien y sigue añadiendo hasta que no queda espacio
        # El espaciado entren alienigenas es de un alien de ancho
        # y otro de alto
        alien: Alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.screen_height - 4 * alien_height):
            while current_x < (self.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Fila terminada; resetea el valor de x e incrementa el de y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position: int, y_position: int) -> None:
        """Crea un alienígena y lo coloca en fila

        Parameters
        ----------
        x_position : int
            _description_
        """
        new_alien: Alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

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
