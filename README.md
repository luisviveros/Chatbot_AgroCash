# 🌾 AgroAsistente Backend

Backend personalizado para el chatbot de WhatsApp AgroAsistente, que ayuda a agricultores a registrar sus gastos e ingresos usando lenguaje natural.

## 📋 Descripción

Sistema que recibe mensajes de WhatsApp a través de Chatwoot, procesa texto y audio con IA (Google Gemini), y almacena transacciones financieras en BigQuery para visualización en Looker Studio.

## 🏗️ Arquitectura

```
WhatsApp → WhatsApp API → Chatwoot → Backend (FastAPI) → Google Cloud
                                          ├─→ Gemini (IA)
                                          ├─→ Speech-to-Text
                                          └─→ BigQuery
```

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11+ con FastAPI
- **IA**: Google Gemini (con Function Calling)
- **Transcripción**: Google Speech-to-Text o OpenAI Whisper
- **Base de Datos**: Google BigQuery
- **Mensajería**: Chatwoot API
- **Dashboard**: Looker Studio

## 📦 Instalación

### 1. Descomprimir el proyecto

```bash
# Si descargaste el ZIP
unzip agroasistente-backend.zip
cd agroasistente-backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Chatwoot
CHATWOOT_API_KEY=tu_api_key_de_chatwoot
CHATWOOT_BASE_URL=https://app.chatwoot.com

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/ruta/a/service-account-key.json
GCP_PROJECT_ID=tu-proyecto-gcp
BIGQUERY_DATASET=agrocash
BIGQUERY_TABLE=gastos

# Gemini
GEMINI_API_KEY=tu_api_key_de_gemini

# Speech-to-Text (elige uno)
STT_PROVIDER=google  # o "openai"
OPENAI_API_KEY=tu_api_key_de_openai  # solo si usas Whisper

# Dashboard
DASHBOARD_URL=https://lookerstudio.google.com/reporting/tu-dashboard-id
```

### 5. Configurar Google Cloud

#### a) Crear Service Account

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Navega a "IAM & Admin" > "Service Accounts"
3. Crea una nueva service account
4. Asigna los roles:
   - BigQuery Data Editor
   - BigQuery User
   - Speech-to-Text User (si usas Google STT)
5. Crea y descarga una clave JSON
6. Coloca el archivo en tu proyecto y actualiza `GOOGLE_APPLICATION_CREDENTIALS`

#### b) Crear Dataset en BigQuery

```sql
CREATE SCHEMA IF NOT EXISTS agrocash;
```

La tabla `gastos` se creará automáticamente al iniciar el servidor.

### 6. Obtener API Keys

- **Gemini**: https://ai.google.dev/
- **Chatwoot**: Settings > Applications > API Access Tokens
- **OpenAI** (opcional): https://platform.openai.com/api-keys

## 🚀 Ejecución

### Desarrollo

```bash
python app/main.py
```

O usando uvicorn directamente:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

El servidor estará disponible en `http://localhost:8000`

## 🔗 Configurar Webhook en Chatwoot

1. Ve a Chatwoot > Settings > Webhooks
2. Crea un nuevo webhook con:
   - **URL**: `https://tu-dominio.com/webhook`
   - **Events**: Selecciona "Message Created"
3. Guarda y activa el webhook

## 📡 API Endpoints

### `GET /`
Endpoint raíz para verificar el estado del servicio.

**Respuesta:**
```json
{
  "service": "AgroAsistente Backend",
  "status": "running",
  "version": "1.0.0"
}
```

### `GET /health`
Health check endpoint.

**Respuesta:**
```json
{
  "status": "healthy"
}
```

### `POST /webhook`
Endpoint principal que recibe webhooks de Chatwoot.

**Payload de ejemplo:**
```json
{
  "event": "message_created",
  "account": {"id": 1},
  "conversation": {"id": 123},
  "message_type": "incoming",
  "content": "gasté 500 en semillas de jitomate",
  "sender": {"phone_number": "+521234567890"}
}
```

## 🧪 Pruebas

### Probar el webhook localmente con ngrok

```bash
# Instalar ngrok
brew install ngrok  # o descarga de https://ngrok.com

# Exponer el puerto local
ngrok http 8000

# Usar la URL de ngrok en Chatwoot
```

### Enviar un webhook de prueba

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "message_created",
    "account": {"id": 1},
    "conversation": {"id": 123},
    "message_type": "incoming",
    "content": "gasté 500 en semillas",
    "sender": {"phone_number": "+521234567890"}
  }'
```

## 📊 Esquema de BigQuery

La tabla `gastos` tiene la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_gasto | STRING | UUID único del gasto |
| id_usuario | STRING | Número de WhatsApp del usuario |
| fecha | TIMESTAMP | Fecha y hora del registro |
| monto | FLOAT | Monto del gasto/ingreso |
| categoria | STRING | Categoría (Semillas, Fertilizantes, etc.) |
| descripcion | STRING | Descripción adicional (opcional) |

## 🤖 Funcionamiento de la IA

### System Prompt
La IA está configurada con instrucciones específicas para:
1. Extraer gastos e ingresos del lenguaje natural
2. Responder a saludos con amabilidad
3. Proporcionar el enlace al dashboard cuando se solicite

### Function Calling (Tools)
La IA utiliza la herramienta `registrar_gasto` que tiene estos parámetros:
- `monto` (número, requerido)
- `categoria` (enum, requerido)
- `descripcion` (string, opcional)

### Categorías Disponibles
- 🌱 Semillas
- 🧪 Fertilizantes
- 💧 Agroquímicos
- 🛠️ Servicios
- 🧑‍🌾 Mano de Obra
- 🚜 Maquinaria
- 🚚 Transporte
- 📦 Empaque
- 🏠 Rentas
- 🏗️ Infraestructura
- 💰 Ingresos

## 🐛 Debugging

### Ver logs en tiempo real

```bash
tail -f logs/app.log  # Si configuras logging a archivo
```

### Verificar conexión con BigQuery

```python
from app.services.bigquery import bigquery_service
bigquery_service.create_table_if_not_exists()
```

### Probar transcripción de audio

```python
from app.services.transcription import transcription_service

with open("audio.ogg", "rb") as f:
    audio_bytes = f.read()
    
text = await transcription_service.transcribe_audio(
    audio_bytes, 
    "audio/ogg"
)
print(text)
```

## 📈 Monitoreo

### Métricas recomendadas
- Tiempo de respuesta del webhook
- Tasa de éxito de transcripciones
- Errores de Gemini
- Inserciones fallidas en BigQuery

### Logs estructurados
El sistema imprime logs con emojis para fácil identificación:
- 📥 Webhook recibido
- 📝 Mensaje de texto
- 🎤 Audio recibido
- ✅ Procesamiento exitoso
- ❌ Error

## 🚀 Despliegue

### Docker (Recomendado)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t agroasistente-backend .
docker run -p 8000:8000 --env-file .env agroasistente-backend
```

### Google Cloud Run

```bash
gcloud run deploy agroasistente-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Seguridad

- ✅ Validación de payloads con Pydantic
- ✅ Manejo de excepciones robusto
- ✅ Variables de entorno para credenciales
- ⚠️ Considera agregar autenticación al webhook (HMAC signature)
- ⚠️ Implementa rate limiting en producción

## 📝 Notas Adicionales

- El sistema es asíncrono para manejar múltiples requests simultáneos
- Los archivos de audio se procesan en memoria (no se guardan en disco)
- BigQuery maneja automáticamente la escala de datos
- Looker Studio se actualiza automáticamente al insertar datos

## 📄 Licencia

MIT License - Uso libre para proyectos comerciales y personales

## 💬 Soporte

Para preguntas o problemas, consulta la documentación incluida:
- FAQ.md para troubleshooting
- EXAMPLES.md para casos de uso
- INDICE.md para navegación completa

---
