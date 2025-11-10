from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============= Modelos de Chatwoot =============

class ChatwootAccount(BaseModel):
    """Cuenta de Chatwoot"""
    id: int


class ChatwootConversation(BaseModel):
    """Conversación de Chatwoot"""
    id: int


class ChatwootAttachment(BaseModel):
    """Archivo adjunto del mensaje"""
    id: int
    file_type: str
    data_url: str


class ChatwootSender(BaseModel):
    """Remitente del mensaje"""
    id: int
    phone_number: Optional[str] = None


class ChatwootWebhookPayload(BaseModel):
    """Payload del webhook de Chatwoot"""
    event: str
    account: ChatwootAccount
    conversation: ChatwootConversation
    message_type: str
    content: Optional[str] = None
    attachments: Optional[List[ChatwootAttachment]] = None
    sender: Optional[ChatwootSender] = None


# ============= Modelos de Gemini =============

class GastoTool(BaseModel):
    """Datos extraídos por la IA para un gasto/ingreso"""
    monto: float = Field(description="El monto numérico del gasto. Ejemplo: 1000")
    categoria: str = Field(
        description="La categoría principal del gasto o ingreso.",
        pattern="^(Semillas 🌱|Fertilizantes 🧪|Agroquímicos 💧|Servicios 🛠️|Mano de Obra 🧑‍🌾|Maquinaria 🚜|Transporte 🚚|Empaque 📦|Rentas 🏠|Infraestructura 🏗️|Ingresos 💰)$"
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Una descripción breve. Ejemplo: 'semilla de jitomate', 'venta de cosecha'"
    )


# ============= Modelos de BigQuery =============

class GastoRecord(BaseModel):
    """Registro completo para insertar en BigQuery"""
    id_gasto: str
    id_usuario: str
    fecha: str  # Formato ISO 8601
    monto: float
    categoria: str
    descripcion: Optional[str] = None


# ============= Respuestas de la API =============

class WebhookResponse(BaseModel):
    """Respuesta del webhook"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
