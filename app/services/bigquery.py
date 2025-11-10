from google.cloud import bigquery
from datetime import datetime
from typing import Dict, Any
import uuid
from app.config import get_settings
from app.models.schemas import GastoRecord


class BigQueryService:
    """Servicio para interactuar con BigQuery"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = bigquery.Client(project=self.settings.gcp_project_id)
        self.table_id = (
            f"{self.settings.gcp_project_id}."
            f"{self.settings.bigquery_dataset}."
            f"{self.settings.bigquery_table}"
        )
    
    async def insert_gasto(
        self,
        id_usuario: str,
        monto: float,
        categoria: str,
        descripcion: str | None = None
    ) -> Dict[str, Any]:
        """
        Inserta un registro de gasto/ingreso en BigQuery
        
        Args:
            id_usuario: ID del usuario (ej: número de WhatsApp)
            monto: Monto del gasto/ingreso
            categoria: Categoría del movimiento
            descripcion: Descripción opcional
            
        Returns:
            Registro insertado con su ID
        """
        try:
            # Generar ID único y fecha
            id_gasto = str(uuid.uuid4())
            fecha = datetime.now().isoformat()
            
            # Crear el registro
            record = GastoRecord(
                id_gasto=id_gasto,
                id_usuario=id_usuario,
                fecha=fecha,
                monto=monto,
                categoria=categoria,
                descripcion=descripcion
            )
            
            # Preparar para BigQuery
            row_to_insert = [record.model_dump()]
            
            # Insertar en BigQuery
            errors = self.client.insert_rows_json(self.table_id, row_to_insert)
            
            if errors:
                print(f"Errores insertando en BigQuery: {errors}")
                raise Exception(f"Error insertando en BigQuery: {errors}")
            
            print(f"✅ Registro insertado exitosamente: {id_gasto}")
            return record.model_dump()
        
        except Exception as e:
            print(f"Error en BigQuery: {e}")
            raise
    
    def create_table_if_not_exists(self):
        """
        Crea la tabla de gastos si no existe (ejecutar en setup inicial)
        """
        schema = [
            bigquery.SchemaField("id_gasto", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("id_usuario", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("fecha", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("monto", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("categoria", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("descripcion", "STRING", mode="NULLABLE"),
        ]
        
        table = bigquery.Table(self.table_id, schema=schema)
        
        try:
            self.client.create_table(table)
            print(f"✅ Tabla creada: {self.table_id}")
        except Exception as e:
            if "Already Exists" in str(e):
                print(f"ℹ️  La tabla ya existe: {self.table_id}")
            else:
                print(f"Error creando tabla: {e}")
                raise


# Instancia global del servicio
bigquery_service = BigQueryService()
