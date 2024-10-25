
# Building... 🚧, stay tuned!

## FarmVibes Client

Este repositorio contiene scripts y notebooks para ejecutar flujos de trabajo usando el cliente de FarmVibes.AI, interactuando con la API de un clúster local o remoto.

## Estructura del Proyecto

- `scripts/`: Aquí se almacenan los scripts para interactuar con la API.
- `data/`: Contiene los archivos de entrada, como geometrías en formato WKT, y los resultados que serán generados.
- `notebooks/`: Incluye notebooks de referencia para entender cómo se ejecutan los flujos de trabajo.
- `requirements.txt`: Archivo que contiene las dependencias necesarias para ejecutar los scripts.

## Requisitos

Python 3.11 es necesario para ejecutar los scripts y notebooks (visitar [python.org](https://www.python.org/downloads/) para descargar la última versión). Ya que necesita usar gdal versionado en src/resources/gdal, se recomienda instalar las dependencias del proyecto en un entorno virtual.


```bash
pipenv shell

```
Despues instalar las dependencias del proyecto.
```bash
pip install -r requirements.txt
pip install .src/resources/GDAL-3.4.3-cp311-cp311-win_amd64.whl

