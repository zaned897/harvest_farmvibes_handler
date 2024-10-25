import requests
from pathlib import Path
from datetime import datetime
from typing import Union, Dict
import logging
import json

logger = logging.getLogger(__name__)

class FarmVibesAPIClient:
    """
    Cliente para interactuar con la API de FarmVibes
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:31108/v0"):
        self.base_url = base_url.rstrip('/')
        
    def _wkt_to_geojson(self, wkt_str: str) -> Dict:
        """
        Convierte WKT a GeoJSON Feature Collection
        """
        # Extraer las coordenadas del WKT
        # Asumimos formato: POLYGON ((-91.838525 42.603940, ...))
        coords_str = wkt_str.replace('POLYGON ((', '').replace('))', '')
        coords = [
            [float(x) for x in pair.strip().split()]
            for pair in coords_str.split(',')
        ]
        
        # Crear el GeoJSON
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    }
                }
            ]
        }

    def create_run(self, 
                   wkt_path: Union[str, Path],
                   start_date: datetime,
                   end_date: datetime,
                   workflow_name: str = "farm_ai/agriculture/ndvi_summary",
                   run_name: str = "ndvi summary") -> Dict:
        """
        Crea una nueva ejecución del workflow
        """
        # Leer el archivo WKT
        wkt_path = Path(wkt_path)
        if not wkt_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo WKT: {wkt_path}")
            
        wkt_str = wkt_path.read_text().strip()
        
        # Preparar el payload
        payload = {
            "name": run_name,
            "workflow": workflow_name,
            "parameters": {},
            "user_input": {
                "start_date": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "geojson": self._wkt_to_geojson(wkt_str)
            }
        }
        
        # Hacer la petición POST
        try:
            response = requests.post(
                f"{self.base_url}/runs",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al hacer la petición: {str(e)}")
            raise

