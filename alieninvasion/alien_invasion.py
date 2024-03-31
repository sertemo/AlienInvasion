from pathlib import Path
import random
import sys
from time import sleep
from typing import Any

import pygame

# from icecream import ic

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

# TODO : puntuacion mas alta permanente en archivo
# TODO : hacer que naves disparen
# TODO : explorar pygame.mixer para sonidos
# TODO : hacer que caigan bonus que den mejoras
# TODO : Escalar el tamaño de las naves restantes


class AlienInvasion:
    """Clase geenral para gestionar los recursos y el comportamiento
    del juego
    """

    def __init__(self) -> None:
        """Inicializa el juego y crea recursos"""
        pygame.init()
        self.clock = pygame.time.Clock()
        # Color de fondo
        self.settings = Settings()

        # Pantalla completa
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.screen_center = self.screen.get_rect().center
        self.background = self.settings.start_background
        # ic(self.screen_center, self.screen_height, self.screen_width)
        # Pantalla con ancho y alto definido en settings
        # self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width, self.settings.screen_height))

        # Crea una instancia para guardar las estadísticas del juego
        # y un marcador
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Crea los elementos del juego
        self.ship = Ship(self)
        self.bullets: Any = pygame.sprite.Group()
        self.aliens: Any = pygame.sprite.Group()

        # Flag para indicar que el juego está activo
        self.game_active = False

        # Crea el botón de play
        self.play_button = Button(
            self,
            "Jugar",
            self.screen_center,
        )
        # Crea un botón de quit
        self.quit_button = Button(
            self,
            "Salir",
            (
                self.screen_center[0],
                self.screen_center[1] + 4 * self.settings.bullet_height,
            ),
        )

        self._create_fleet()

    def run_game(self) -> None:
        """Inicia el bucle principal del juego"""
        while True:
            # Busca eventos de teclado y ratón
            self._check_events()

            if self.game_active:
                # Actualiza la posición de la nave
                self.ship.update()
                # Actualizamos las balas
                self._update_bullets()
                # Actualizamos la posición de los aliens
                self._update_aliens()
                # Actualizamos la pantalla

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _load_background(self) -> Path:
        """Devuelve la ruta a un fondo aleatorio
        de la carpeta fondos

        Returns
        -------
        Path
            _description_
        """
        fondos: list[Path] = list(self.settings.bg_img_path.iterdir())
        return random.choice(fondos)

    def _check_events(self) -> None:
        """Responde a pulsaciones de teclas y eventos de ratón"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _start_game(self) -> None:
        """Inicia el juego"""
        # Restablece las estadisticas del juego
        self.stats.reset_stats()
        self.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Se deshace de los aliens y las balas que queda
        self.aliens.empty()
        self.bullets.empty()

        # Crea un nuevo fondo
        self.background = self._load_background()
        # Crea una flota nueva y centra la nave.
        self._create_fleet()
        self.ship.center_ship()

        # Restablece las configuraciones de velocidad
        self.settings.initialize_dynamic_settings()

        # Oculta el ratón
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """Inicia el juego cuando el jugador
        hace clic en play

        Parameters
        ----------
        mouse_pos : tuple[int, int]
            _description_
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _check_quit_button(self, mouse_pos: tuple[int, int]) -> None:
        """Sale dle juego cuando el jugador hace clic
        en Salir

        Parameters
        ----------
        mouse_pos : tuple[int, int]
            _description_
        """
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            sys.exit(0)

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
        # Iniciamos el juego con la tecla J
        elif event.key == pygame.K_j and not self.game_active:
            self._start_game()

    def _fire_bullet(self) -> None:
        """Crea una nueva bala y la añade al grupo de balas"""
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
        """Actualiza la posición de las balas y se deshace de las viejas"""
        self.bullets.update()

        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Busca balas que hayan dado a un alien
        # Si hay se deshace de la bala y el alien
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self) -> None:
        """Responde a las colisiones bala-alien"""
        # Retira las balas y aliens que han chocado
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Subimos de nivel
            # Destruye las balas existentes y crea una flota nueva.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Cargamos otro fondo
            self.background = self._load_background()
            # Aumentamos el nivel
            self.stats.level += 1
            self.sb.prep_level()

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
        """Responde al impacto de un alien en la nave"""
        if self.stats.ships_left > 0:
            # Disminuye ships_left
            self.stats.ships_left -= 1
            # Actualiza el marcador
            self.sb.prep_ships()

            # Se deshace de aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False
            # Volvemos a hacer visible el ratón
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self) -> None:
        """Comprueba si algún alien ha llegado al fondo de la pantalla"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_height:
                # Trata esto como si la nave hubiese sido alcanzada
                self._ship_hit()
                break

    def _check_fleet_edges(self) -> None:
        """Responde adecuadamente si algún alien ha llegado al borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Baja toda la flota y cambia su dirección"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self) -> None:
        """Crea una flota de aliens."""
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
        # Para color de fondo
        # self.screen.fill(self.settings.bg_color)

        # Para imágen de fondo
        # Cargar la imagen de fondo
        fondo = pygame.image.load(self.background).convert()
        # Redimensionar la imagen para que coincida
        # con el tamaño de la pantalla
        fondo = pygame.transform.scale(fondo, (self.screen_width, self.screen_height))
        # Pintamos la imagen
        self.screen.blit(fondo, (0, 0))

        self.ship.blitme()
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Dibuja la información de la puntuación
        self.sb.show_score()

        # Dibuja el botón para jugar si el juego está inactivo
        if not self.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()

        # Hace visible la ultima pantalla dibujada
        pygame.display.flip()


if __name__ == "__main__":

    ai = AlienInvasion()
    ai.run_game()
