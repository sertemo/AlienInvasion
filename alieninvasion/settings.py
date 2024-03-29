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
        self.fps = 60

        # Configuración de la nave
        self.ship_speed: int = 5

        # Configuración de las balas
        self.bullet_speed = 8
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (57, 255, 20)
        self.bullets_allowed = 3

        # Configuración de los aliens
        self.alien_path = Path('alieninvasion/images/alien')
