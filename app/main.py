from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.config import get_settings
from app.models.schemas import ChatwootWebhookPayload, WebhookResponse
from app.handlers.webhook import webhook_handler
from app.services.bigquery import bigquery_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    print("🚀 Iniciando AgroAsistente Backend...")
    settings = get_settings()
    print(f"✅ Configuración cargada")
    print(f"   - Chatwoot: {settings.chatwoot_base_url}")
    print(f"   - BigQuery: {settings.gcp_project_id}.{settings.bigquery_dataset}.{settings.bigquery_table}")
    print(f"   - STT Provider: {settings.stt_provider}")
    
    # Verificar que la tabla de BigQuery existe
    try:
        bigquery_service.create_table_if_not_exists()
    except Exception as e:
        print(f"⚠️  Advertencia al verificar tabla BigQuery: {e}")
    
    yield
    
    # Shutdown
    print("👋 Cerrando AgroAsistente Backend...")


app = FastAPI(
    title="AgroAsistente Backend",
    description="Backend para el chatbot de WhatsApp AgroAsistente",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servidor está funcionando"""
    return {
        "service": "AgroAsistente Backend",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/webhook", response_model=WebhookResponse)
async def webhook_endpoint(request: Request):
    """
    Endpoint principal que recibe los webhooks de Chatwoot
    
    Este endpoint:
    1. Recibe notificaciones de mensajes desde Chatwoot
    2. Determina si es texto o audio
    3. Transcribe el audio si es necesario
    4. Procesa con Gemini
    5. Registra en BigQuery o responde al usuario
    """
    try:
        # Obtener el payload
        payload_dict = await request.json()
        
        # Log para debugging
        print(f"\n{'='*60}")
        print(f"📥 Webhook recibido de Chatwoot")
        print(f"   Event: {payload_dict.get('event')}")
        print(f"   Message Type: {payload_dict.get('message_type')}")
        print(f"{'='*60}\n")
        
        # Validar y parsear con Pydantic
        payload = ChatwootWebhookPayload(**payload_dict)
        
        # Procesar el webhook
        result = await webhook_handler.process_webhook(payload)
        
        return WebhookResponse(
            success=result["success"],
            message=result["message"],
            data=result.get("data")
        )
    
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        print(f"❌ Error interno: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    print(f"❌ Excepción no manejada: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True  # Solo para desarrollo
    )
