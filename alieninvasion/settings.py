from pathlib import Path


class Settings:
    """Una clase para guardar toda la configuración de Alien
    Invasion
    """

    def __init__(self) -> None:
        """Inicializa la configuración del juego"""
        # Configuraciones estáticas
        self.font = "Poppins"
        # Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (130, 130, 130)
        self.bg_img_path = Path("alieninvasion/images/background")
        self.start_background = Path("alieninvasion/images/start_background.png")
        self.fps = 60

        # Configuración de puntuación
        self.alien_points = 50
        self.score_color = (180, 255, 180)
        self.game_over_color = (255, 255, 250)
        self.high_score_path = Path("db/HighScore.txt")

        # Configuración de los botones
        self.button_width = 200
        self.button_height = 80

        # Configuración de la nave
        self.ship_limit: int = 3

        # Configuración de las balas
        self.bullet_width = 4
        self.bullet_height = 30
        self.bullet_color = (57, 255, 20)
        self.bullet_color_alien = (255, 10, 24)
        self.bullets_allowed = 3

        # Configuración de los aliens
        self.alien_path = Path("alieninvasion/images/alien")
        self.fleet_drop_speed = 12  # velocidad de bajada de la flota

        # Rapidez con la que se acelera el juego
        self.speedup_scale = 1.2
        # Lo rápido que aumentan los puntos conseguidos
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Inicializa las configuraciones que cambian
        durante el juego al incrementar dificultad
        """
        self.ship_speed: float = 6.5
        self.bullet_speed: float = 10.0
        self.bullet_alien_speed: float = 9.0
        self.alien_speed: float = 7.0
        self.alien_fire_rate = 0.5
        # Dirección de la flota 1: derecha -1: izquierda
        self.fleet_direction = 1

    def increase_speed(self) -> None:
        """Incrementa las configuraciones de velocidad y los valores
        de los puntos al subir de nivel
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
