from enum import Enum
from pathlib import Path
from typing import Union
from pydantic import BaseModel
import logging
from osgeo import ogr, osr
import json

logger = logging.getLogger(__name__)

class FileType(str, Enum):
    KML = ".kml"
    SHP = ".shp"
    GEOJSON = ".geojson"
    WKT = ".wkt"

class GeometricConverter:
    """
    Clase para convertir diferentes formatos geométricos a WKT usando GDAL/OGR.
    """
    
    def __init__(self):
        self._supported_extensions = {
            FileType.KML.value,
            FileType.SHP.value,
            FileType.GEOJSON.value,
            FileType.WKT.value
        }
        # Registrar todos los drivers de OGR
        ogr.RegisterAll()

    def convert_to_wkt(self, input_path: Union[str, Path]) -> str:
        """
        Convierte un archivo de entrada a formato WKT usando GDAL/OGR.
        
        Args:
            input_path: Ruta al archivo de entrada
            
        Returns:
            str: Representación WKT de la geometría
            
        Raises:
            ValueError: Si el formato de archivo no es soportado
            FileNotFoundError: Si el archivo no existe
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {input_path}")
            
        extension = input_path.suffix.lower()
        
        if extension not in self._supported_extensions:
            raise ValueError(
                f"Formato no soportado: {extension}. "
                f"Formatos soportados: {', '.join(self._supported_extensions)}"
            )

        try:
            # Abrir el archivo de entrada
            datasource = ogr.Open(str(input_path))
            if datasource is None:
                raise ValueError(f"No se pudo abrir el archivo: {input_path}")

            # Obtener la primera capa
            layer = datasource.GetLayer(0)
            if layer is None:
                raise ValueError("No se encontró ninguna capa en el archivo")

            # Obtener el primer feature
            feature = layer.GetNextFeature()
            if feature is None:
                raise ValueError("No se encontró ninguna geometría en la capa")

            # Obtener la geometría
            geom = feature.GetGeometryRef()
            if geom is None:
                raise ValueError("La geometría es nula")

            # Convertir a WKT
            wkt = geom.ExportToWkt()
            
            # Limpiar
            feature = None
            layer = None
            datasource = None
            
            return wkt

        except Exception as e:
            logger.error(f"Error al convertir archivo: {str(e)}")
            raise

    def save_wkt(
        self,
        wkt_str: str,
        output_path: Union[str, Path],
        create_dirs: bool = True
    ) -> Path:
        """
        Guarda una cadena WKT en un archivo.
        
        Args:
            wkt_str: String WKT a guardar
            output_path: Ruta donde guardar el archivo
            create_dirs: Si crear directorios intermedios
            
        Returns:
            Path: Ruta del archivo guardado
        """
        output_path = Path(output_path)
        
        if create_dirs:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Validar que es un WKT válido usando OGR
            geom = ogr.CreateGeometryFromWkt(wkt_str)
            if geom is None:
                raise ValueError("WKT inválido")

            # Guardar el WKT
            output_path.write_text(wkt_str)
            return output_path
            
        except Exception as e:
            logger.error(f"Error al guardar WKT: {str(e)}")
            raise

    def reproject_geometry(self, geom: ogr.Geometry, 
                         source_epsg: int = 4326, 
                         target_epsg: int = 4326) -> ogr.Geometry:
        """
        Reproyecta una geometría de un sistema de coordenadas a otro.
        
        Args:
            geom: Geometría de OGR
            source_epsg: Código EPSG del sistema de coordenadas fuente
            target_epsg: Código EPSG del sistema de coordenadas destino
        
        Returns:
            ogr.Geometry: Geometría reproyectada
        """
        if source_epsg == target_epsg:
            return geom

        # Crear las referencias espaciales
        source_srs = osr.SpatialReference()
        source_srs.ImportFromEPSG(source_epsg)

        target_srs = osr.SpatialReference()
        target_srs.ImportFromEPSG(target_epsg)

        # Crear la transformación
        transform = osr.CoordinateTransformation(source_srs, target_srs)

        # Clonar y transformar la geometría
        geom_clone = geom.Clone()
        geom_clone.Transform(transform)

        return geom_clone

