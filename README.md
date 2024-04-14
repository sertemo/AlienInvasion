# Alien Invasion v0.1.0
![Tests](https://github.com/sertemo/AlienInvasion/actions/workflows/tests.yml/badge.svg)

Proyecto del libro **Curso intensivo de Python** para crear un juego tipo Space Invaders utilizando **pygame**.
- Se usa **Flake8** para seguir las directrices de PEP8
- Se usa **mypy** para un correcto typehinting
- **Black** para el formateo del código
- **Pytest** para testear el código

## Juego
![alt text](<alieninvasion/images/alieninvasion.png>)

## Updates
- 06/04/2024
    - Los aliens disparan con una cadencia configurable que aumenta con el nivel de juego
    - Caen bonus cada cierto tiempo con mejoras para la nave
    - Se aplican mejoras de velocidad de número de balas máximas y de vida extra
    - Se aplican imágenes de los bonus
- 09/04/2024
    - Se añade un mensaje con las stats de bonus conseguidas en el game over
- 11/04/2024
    - Se añaden algunos sonidos
- 14/04/2024
    - Se añade animación de explosión

## Posibles Mejoras
- Mejorar la animación de la explosión haciendo que se desplace en la dirección de los aliens
- Implementar un pequeño texto de ("speed up" o "life up" o "bullets up") al recoger un bonus