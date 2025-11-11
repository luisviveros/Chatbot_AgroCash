from google.cloud import bigquery
from datetime import datetime
from typing import Dict, Any
import uuid
from app.config import get_settings


class BigQueryService:
    """Servicio para interactuar con BigQuery"""
    
    # Mapeo de categorías a IDs de subcategorías
    CATEGORIA_TO_SUBCATEGORIA = {
        "Semillas 🌱": "sub-001",
        "Fertilizantes 🧪": "sub-002",
        "Agroquímicos 💧": "sub-003",
        "Servicios 🛠️": "sub-004",
        "Mano de Obra 🧑‍🌾": "sub-005",
        "Maquinaria 🚜": "sub-006",
        "Transporte 🚚": "sub-007",
        "Empaque 📦": "sub-008",
        "Rentas 🏠": "sub-009",
        "Infraestructura 🏗️": "sub-010",
        "Ingresos 💰": "sub-011",
    }
    
    def __init__(self):
        self.settings = get_settings()
        self.client = bigquery.Client(project=self.settings.gcp_project_id)
        self.dataset = self.settings.bigquery_dataset
        self.table_gastos = f"{self.settings.gcp_project_id}.{self.settings.bigquery_dataset}.gastos"
        self.table_ingresos = f"{self.settings.gcp_project_id}.{self.settings.bigquery_dataset}.ingresos"
    
    def _get_subcategoria_id(self, categoria: str) -> str:
        """Obtiene el ID de subcategoría basado en la categoría"""
        return self.CATEGORIA_TO_SUBCATEGORIA.get(categoria, "sub-001")  # Default a Semillas
    
    async def insert_gasto(
        self,
        id_usuario: str,
        monto: float,
        categoria: str,
        descripcion: str | None = None
    ) -> Dict[str, Any]:
        """
        Inserta un registro de gasto o ingreso en BigQuery
        
        Args:
            id_usuario: ID del usuario (ej: número de WhatsApp)
            monto: Monto del gasto/ingreso
            categoria: Categoría del movimiento
            descripcion: Descripción opcional
            
        Returns:
            Registro insertado con su ID
        """
        try:
            # Determinar si es ingreso o gasto
            es_ingreso = "Ingreso" in categoria or "💰" in categoria
            
            # Generar ID único y fecha
            id_registro = str(uuid.uuid4())
            fecha = datetime.now().date().isoformat()
            
            # Obtener ID de subcategoría
            id_subcategoria = self._get_subcategoria_id(categoria)
            
            # Crear el registro
            record = {
                "id_gasto" if not es_ingreso else "id_ingreso": id_registro,
                "id_usuario": id_usuario,
                "id_subcategoria": id_subcategoria,
                "fecha": fecha,
                "descripcion": descripcion or categoria,
                "monto": float(monto)
            }
            
            # Seleccionar tabla correcta
            table_id = self.table_ingresos if es_ingreso else self.table_gastos
            
            # Preparar para BigQuery
            row_to_insert = [record]
            
            # Insertar en BigQuery
            errors = self.client.insert_rows_json(table_id, row_to_insert)
            
            if errors:
                print(f"Errores insertando en BigQuery: {errors}")
                raise Exception(f"Error insertando en BigQuery: {errors}")
            
            tipo = "Ingreso" if es_ingreso else "Gasto"
            print(f"✅ {tipo} insertado exitosamente: {id_registro}")
            print(f"   Subcategoría: {id_subcategoria} ({categoria})")
            print(f"   Tabla: {table_id}")
            return record
        
        except Exception as e:
            print(f"Error en BigQuery: {e}")
            raise
    
    def create_table_if_not_exists(self):
        """
        Verifica que las tablas existan
        """
        try:
            # Verificar tabla de gastos
            table_gastos = self.client.get_table(self.table_gastos)
            print(f"ℹ️  Tabla gastos existe: {self.table_gastos}")
            print(f"   Campos: {[field.name for field in table_gastos.schema]}")
            
            # Verificar tabla de ingresos
            table_ingresos = self.client.get_table(self.table_ingresos)
            print(f"ℹ️  Tabla ingresos existe: {self.table_ingresos}")
            print(f"   Campos: {[field.name for field in table_ingresos.schema]}")
            
        except Exception as e:
            if "Not found" in str(e):
                print(f"⚠️  Tabla no encontrada. Asegúrate de que existan las tablas:")
                print(f"   - {self.table_gastos}")
                print(f"   - {self.table_ingresos}")
            else:
                print(f"Error verificando tablas: {e}")


# Instancia global del servicio
bigquery_service = BigQueryService()
