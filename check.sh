#!/bin/bash

# Define colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # Sin color

# Define la variable project_path con el path de tu proyecto
project_path="alieninvasion/"

echo -e "${YELLOW}Ejecutando Black...${NC}"
poetry run black "$project_path"
echo -e "${GREEN}Black finalizado correctamente.${NC}"

echo -e "${YELLOW}Ejecutando MyPy...${NC}"
poetry run mypy "$project_path"
echo -e "${GREEN}MyPy finalizado correctamente.${NC}"

echo -e "${YELLOW}Ejecutando Flake8...${NC}"
if poetry run flake8 "$project_path"; then
    echo -e "${GREEN}Flake8 finalizado correctamente. No se encontraron problemas.${NC}"
else
    echo -e "${RED}Flake8 encontró problemas.${NC}"
fi

# ejecutar chmod +x tests.sh para hacer el archivo ejecutable: ./tests.sh

