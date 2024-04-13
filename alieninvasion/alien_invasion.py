from pathlib import Path
import random
import sys
from time import sleep
from typing import Any, Union

import pygame

from icecream import ic

from alien import Alien
from bonus import Bonus
from bullet import Bullet
from button import Button
from explosion import Explosion
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

# TODO : Cargar más fondos


class AlienInvasion:
    """Clase geenral para gestionar los recursos y el comportamiento
    del juego
    """

    def __init__(self) -> None:
        """Inicializa el juego y crea recursos"""
        pygame.init()
        pygame.mixer.init()

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
        self.alien_bullets: Any = pygame.sprite.Group()
        self.aliens: Any = pygame.sprite.Group()
        self.bonuses: Any = pygame.sprite.Group()
        self.explosions: Any = pygame.sprite.Group()

        # Creamos el evento periódico de disparo de balas
        # De los aliens
        self.SHOOT_EVENT = pygame.USEREVENT + 1
        # Cada 5 s
        pygame.time.set_timer(self.SHOOT_EVENT, 1000)

        # Creamos el evento de los Bonus
        self.FALL_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.FALL_EVENT, self.settings.bonus_rate)
        self.SPEED_BONUS_EVENT: Union[None, int] = None
        self.BULLET_BONUS_EVENT: Union[None, int] = None

        # Flag para indicar que el juego está activo
        self.game_active = False

        # Sonidos
        self.shoot_sound_ship = pygame.mixer.Sound(
            "data/sounds/Futuristic Shotgun Single Shot.wav"
        )
        self.shoot_sound_ship.set_volume(0.3)
        self.shoot_sound_alien_ship = pygame.mixer.Sound("data/sounds/Laser Shot.wav")
        self.entry_music = pygame.mixer.Sound("data/sounds/entradilla.ogg")
        self.level_up_sound = pygame.mixer.Sound("data/sounds/level_up.wav")
        self.level_up_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound("data/sounds/explosion.ogg")
        self.explosion_sound.set_volume(0.4)
        self.pick_bonus_sound = pygame.mixer.Sound("data/sounds/41_enginespeedup.wav")
        self.falling_bonus_sound = pygame.mixer.Sound("data/sounds/16_falling.wav")
        self.game_over_sound = pygame.mixer.Sound("data/sounds/GAMEOVER.wav")

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
                # Actualiza la posición de los bonus
                self._update_bonus()

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
            elif (event.type == self.SHOOT_EVENT) and self.game_active:
                # Alien dispara balas con cierta probabilidad
                if random.random() < self.settings.alien_fire_rate:
                    self._alien_fire_bullet()
            elif (event.type == self.FALL_EVENT) and self.game_active:
                self._create_bonus()
            elif (event.type == self.BULLET_BONUS_EVENT) and self.game_active:
                # Revertimos el efecto del bono de las balas
                self.end_bonus_bullets()
            elif (event.type == self.SPEED_BONUS_EVENT) and self.game_active:
                # Revertimos el efecto del bono de las balas
                self.end_bonus_speed()

    def _start_game(self) -> None:
        """Inicia el juego"""
        # Reproduce entradilla
        self.entry_music.play()
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

    def game_over(self) -> None:
        """Muestra un mensaje de Game Over en la pantalla
        cuando se acaban las vidas
        """
        # Reproduce el sonido
        game_over_msg = "Game Over"
        font = pygame.font.SysFont(self.settings.font, 150)
        game_over_image = font.render(
            game_over_msg, True, self.settings.game_over_color
        )

        # Centra la puntuación en la parte superior de la pantalla
        game_over_rect = game_over_image.get_rect()
        game_over_rect.centerx = self.screen_width // 2
        game_over_rect.top = 280

        # Muestra el texto
        self.screen.blit(game_over_image, game_over_rect)

        bonus_stats_msg = f"Extra speed: {self.stats.bonus_stats['extra_speed']}\
        Extra bullets: {self.stats.bonus_stats['extra_bullets']} \
        Extra life: {self.stats.bonus_stats['extra_life']}"
        font = pygame.font.SysFont(self.settings.font, 70)
        bonus_stats_image = font.render(
            bonus_stats_msg, True, self.settings.game_over_color
        )

        bonus_stats_rect = bonus_stats_image.get_rect()
        bonus_stats_rect.centerx = self.screen_width // 2
        bonus_stats_rect.bottom = self.screen_height - 100

        self.screen.blit(bonus_stats_image, bonus_stats_rect)

    def _exit_game(self) -> None:
        """Guarda el high score en db y cierra el juego"""
        # Guardamos el highscore
        self.stats.save_highscore()
        sys.exit(0)

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
            self._exit_game()

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
            self._exit_game()
        # Iniciamos el juego con la tecla J
        elif event.key == pygame.K_j and not self.game_active:
            self._start_game()

    def _fire_bullet(self) -> None:
        """Crea una nueva bala y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # Reproducimos sonido de disparo
            self.shoot_sound_ship.play()

    def _alien_fire_bullet(self) -> None:
        """Simula el disparo de un alien. Crea una nueva
        bala de tipo alien
        """
        new_bullet = Bullet(self, type="alien")
        self.alien_bullets.add(new_bullet)
        self.shoot_sound_alien_ship.play()

    def _create_bonus(self) -> None:
        """Crea un nuevo bonus de forma aleatoria"""
        bonus_type = random.choice(self.settings.bonus_type_list)
        new_bonus = Bonus(self, type=bonus_type)
        self.bonuses.add(new_bonus)
        # Reproduce el sonido
        self.falling_bonus_sound.play()

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
        """Actualiza la posición de todas las balas
        y se deshace de las viejas"""
        self.bullets.update()
        self.alien_bullets.update()

        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.screen_height:
                self.alien_bullets.remove(alien_bullet)

        # Busca balas que hayan dado a un alien
        # Si hay se deshace de la bala y el alien
        self._check_bullet_alien_collisions()

        # Comprueba si alguna bala ha dado a la nave
        self._check_alien_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self) -> None:
        """Responde a las colisiones bala-alien"""
        # Retira las balas y aliens que han chocado
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            # Reproducimos el sonido
            self.explosion_sound.play()
            for aliens in collisions.values():
                # TODO Meter aqui animación de Explosión
                ic(aliens)
                for alien in aliens:
                    # Sacar la posición del alien
                    center = alien.rect.center
                    ic(center)
                    # Creamos la explosión
                    explosion = Explosion(center)
                    self.explosions.add(explosion)
                    # Añadimos a la lista

                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Subimos de nivel
            # Reproducimos musiquilla
            self.level_up_sound.play()
            # Destruye las balas existentes y crea una flota nueva.
            self.bullets.empty()
            self.alien_bullets.empty()
            self.bonuses.empty()

            # Printea las stats de bonus
            ic(self.stats.bonus_stats)

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

    def _update_bonus(self) -> None:
        """Actualiza la posición de los bonus. Hacia abajo"""
        self.bonuses.update()

        # Comprueba si ha habido colsion con la nave
        self._check_bonus_ship_collision()

    def _check_bonus_ship_collision(self) -> None:
        """Responde a la colisión de la nave con el bonus"""
        collisions = pygame.sprite.spritecollide(self.ship, self.bonuses, True)

        if collisions:
            # Reproducimos el sonido
            self.pick_bonus_sound.play()
            # Sacamos el tipo de bonus que hemos cogido
            bonus_type = collisions[0].type
            # Añadimos a la estadísticas
            self.stats.bonus_stats[bonus_type] += 1
            # Se lo pasamos a la función para gestionar los bonus
            self.apply_bonus(bonus_type)

    def apply_bonus(self, bonus_type: str) -> None:
        """Gestiona las mejores del bono en el jugador
        cuando la nave recoge el bono
        """

        # Creamos un evento de bono en función del tipo
        ic(f"Aplicado bono tipo {bonus_type}")
        if bonus_type == "extra_bullets":
            self.BULLET_BONUS_EVENT = pygame.USEREVENT + 10
            pygame.time.set_timer(
                self.BULLET_BONUS_EVENT, 10_000, True
            )  # True dura solo 1 vez
            # Aplicamos la mejora
            self._apply_extra_bullets()
        elif bonus_type == "extra_speed":
            self.SPEED_BONUS_EVENT = pygame.USEREVENT + 11
            pygame.time.set_timer(self.SPEED_BONUS_EVENT, 5000, True)
            # Aplicamos la mejora
            self._apply_extra_speed()
        elif bonus_type == "extra_life":
            self._apply_extra_life()

    def _apply_extra_speed(self) -> None:
        """Aplica el aumento de velocidad de la nave"""
        self.settings.ship_speed += self.settings.extra_speed

    def _apply_extra_bullets(self) -> None:
        """Aumenta el número de balas permitidas"""
        self.settings.bullets_allowed += self.settings.extra_bullets

    def _apply_extra_life(self) -> None:
        """Aumenta el número de naves"""
        self.stats.ships_left += 1
        # Actualizamos el marcador
        self.sb.prep_ships()

    def end_bonus_bullets(self) -> None:
        """Revierte las mejores aplicadas con el bonus de las balas"""
        self.settings.bullets_allowed -= self.settings.extra_bullets

    def end_bonus_speed(self) -> None:
        """Revierte las mejores aplicadas con el bonus de las balas"""
        self.settings.ship_speed -= self.settings.extra_speed

    def _check_alien_bullet_ship_collisions(self) -> None:
        """Response a las colisiones de las balas
        de los aliens con la nave
        """
        collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)

        if collisions:
            self._ship_hit()

    def _ship_hit(self) -> None:
        """Responde al impacto de un alien en la nave"""
        # Reproducimos sonido de explosion
        self.explosion_sound.play()
        if self.stats.ships_left > 0:
            # Disminuye ships_left
            self.stats.ships_left -= 1
            # Actualiza el marcador
            self.sb.prep_ships()

            # Se deshace de aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.bonuses.empty()

            # Quita los bonus
            # TODO

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
        else:
            self.game_active = False
            # Volvemos a hacer visible el ratón
            pygame.mouse.set_visible(True)
            self.game_over_sound.play()

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
        while current_y < (self.screen_height - 5 * alien_height):
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
        # Dibujamos las explosiones
        self.explosions.update() # TODO Comprobarlo
        self.explosions.draw() # TODO Comprobarlo
        # Dibujamos balas de la nave
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Dibujamos balas de los aliens
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()
        # Dibujamos bonus
        self.bonuses.draw(self.screen)

        # Dibuja la información de la puntuación
        self.sb.show_score()

        # Dibuja el botón para jugar si el juego está inactivo
        if not self.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()
            # Si no quedan vidas mostramos Game Over
            if self.stats.ships_left == 0:
                self.game_over()

        # Hace visible la ultima pantalla dibujada
        pygame.display.flip()


if __name__ == "__main__":

    ai = AlienInvasion()
    ai.run_game()
