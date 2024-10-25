# main.py
from pathlib import Path
from datetime import datetime
import logging
import json
from src.api_client import FarmVibesAPIClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Definir rutas y parámetros
        base_dir = Path(__file__).parent
        wkt_file = base_dir / "data" / "output" / "corn_site_1.wkt"
        
        # Definir rango de fechas para mayo 2024
        start_date = datetime(2024, 5, 1)
        end_date = datetime(2024, 5, 31)
        
        # Configurar el cliente
        client = FarmVibesAPIClient()
        
        # Crear y ejecutar el workflow
        logger.info(f"Iniciando workflow NDVI para el archivo: {wkt_file}")
        logger.info(f"Periodo: {start_date.date()} - {end_date.date()}")
        
        response = client.create_run(
            wkt_path=wkt_file,
            start_date=start_date,
            end_date=end_date,
            workflow_name="farm_ai/agriculture/ndvi_summary",
            run_name="NDVI Summary - Mayo 2024"
        )
        
        # Imprimir la respuesta
        logger.info("Workflow iniciado exitosamente")
        logger.info(f"Respuesta de la API: {json.dumps(response, indent=2)}")

    except Exception as e:
        logger.error(f"Error durante la ejecución: {str(e)}")
        raise

if __name__ == "__main__":
    main()

