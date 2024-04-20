# Utilizar una imagen base oficial de Python
FROM python:3.10-slim

# Instalar dependencias del sistema para Pygame
RUN apt-get update && apt-get install -y \
    python3-sdl2 \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libsdl1.2-dev \
    libportmidi-dev \
    libfreetype6-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff5-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Configurar el entorno para que los paquetes se instalen globalmente
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar Poetry
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python -

# No crear un entorno virtual con Poetry
RUN poetry config virtualenvs.create false

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar dependencias usando Poetry
RUN poetry install --only main

# Copiar el resto del código fuente de la aplicación
COPY . /app

# Comando para ejecutar la aplicación, ajustar según sea necesario
CMD ["poetry", "run", "python", "alieninvasion/alien_invasion.py"]
