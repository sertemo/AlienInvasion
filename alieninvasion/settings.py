from pathlib import Path


class Settings:
    """Una clase para guardar toda la configuración de Alien
    Invasion
    """

    def __init__(self) -> None:
        """Inicializa la configuración del juego
        """

        # Configuración de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (130, 130, 130)
        self.bg_color_img = Path(
            'alieninvasion/images/background/background.jpg'
            )
        self.fps = 60

        # Configuración de los botones
        self.button_width = 200
        self.button_height = 80

        # Configuración de la nave
        self.ship_speed: int = 8
        self.ship_limit: int = 3

        # Configuración de las balas
        self.bullet_speed = 10
        self.bullet_width = 3
        self.bullet_height = 30
        self.bullet_color = (57, 255, 20)
        self.bullets_allowed = 3

        # Configuración de los aliens
        self.alien_path = Path('alieninvasion/images/alien')
        self.alien_speed = 10.0
        self.fleet_drop_speed = 20  # velocidad de bajada de la flota
        # Dirección de la flota 1: derecha -1: izquierda
        self.fleet_direction = 1
