# 🚀 Guía de Inicio Rápido - AgroAsistente

## Pasos para poner en marcha el sistema

### 1️⃣ Configuración Inicial (5 minutos)

```bash
# Clonar o descargar el proyecto
cd agroasistente-backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar Variables de Entorno (10 minutos)

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env  # o usa tu editor favorito
```

**Lo que necesitas:**

1. **Chatwoot API Key**: 
   - Ve a Chatwoot → Settings → Applications → API Access Tokens
   - Crea un token nuevo
   
2. **Gemini API Key**: 
   - Visita https://ai.google.dev/
   - Obtén tu API key gratuita
   
3. **Google Cloud Service Account**:
   - Ve a https://console.cloud.google.com
   - Crea un proyecto (si no tienes uno)
   - Habilita BigQuery API y Speech-to-Text API
   - Crea una Service Account con permisos de BigQuery
   - Descarga el archivo JSON de credenciales
   - Colócalo en una carpeta segura
   
4. **(Opcional) OpenAI API Key**:
   - Solo si prefieres usar Whisper en lugar de Google Speech-to-Text
   - https://platform.openai.com/api-keys

### 3️⃣ Crear Dataset en BigQuery (2 minutos)

Ve a [BigQuery Console](https://console.cloud.google.com/bigquery) y ejecuta:

```sql
CREATE SCHEMA IF NOT EXISTS agrocash;
```

La tabla se creará automáticamente al iniciar el servidor.

### 4️⃣ Ejecutar el Servidor (1 minuto)

```bash
python app/main.py
```

Deberías ver:
```
🚀 Iniciando AgroAsistente Backend...
✅ Configuración cargada
   - Chatwoot: https://app.chatwoot.com
   - BigQuery: tu-proyecto.agrocash.gastos
   - STT Provider: google
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5️⃣ Probar Localmente (2 minutos)

En otra terminal:

```bash
# Activar el entorno virtual
source venv/bin/activate

# Ejecutar pruebas
python test_webhook.py
```

### 6️⃣ Exponer el Servidor (5 minutos)

Para que Chatwoot pueda enviar webhooks, necesitas una URL pública:

#### Opción A: ngrok (Desarrollo)

```bash
# Instalar ngrok
brew install ngrok  # Mac
# O descarga de https://ngrok.com

# Exponer el puerto
ngrok http 8000

# Copia la URL que aparece (ej: https://abc123.ngrok.io)
```

#### Opción B: Cloud Run (Producción)

```bash
gcloud run deploy agroasistente-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 7️⃣ Configurar Webhook en Chatwoot (3 minutos)

1. Ve a Chatwoot → Settings → Webhooks
2. Click en "Add Webhook"
3. Configura:
   - **URL**: `https://tu-url.ngrok.io/webhook` (o tu URL de producción)
   - **Events**: Marca "Message Created"
4. Guarda

### 8️⃣ ¡Probar en WhatsApp! 🎉

Envía mensajes a tu número de WhatsApp conectado a Chatwoot:

```
"gasté 500 en semillas"
"vendí la cosecha por 15000"
"quiero ver el dashboard"
```

---

## 🆘 Troubleshooting

### El webhook no responde

1. Verifica que el servidor esté corriendo: `curl http://localhost:8000/health`
2. Revisa los logs del servidor
3. Verifica que ngrok esté activo

### Error de BigQuery

```bash
# Verificar credenciales
echo $GOOGLE_APPLICATION_CREDENTIALS

# Probar conexión
python -c "from app.services.bigquery import bigquery_service; bigquery_service.create_table_if_not_exists()"
```

### Error de Gemini

- Verifica que tu API key sea válida
- Asegúrate de tener cuota disponible en https://ai.google.dev/

### Error de transcripción

- Verifica que tengas habilitada la API de Speech-to-Text
- O cambia a OpenAI Whisper en el `.env`: `STT_PROVIDER=openai`

---

## 📚 Siguientes Pasos

1. ✅ Revisa el [README.md](README.md) completo
2. ✅ Personaliza el System Prompt en `app/services/gemini.py`
3. ✅ Configura tu dashboard de Looker Studio
4. ✅ Implementa autenticación del webhook (HMAC)
5. ✅ Configura monitoreo y alertas

---

## 💡 Tips Pro

- Usa `uvicorn app.main:app --reload` para recargar automáticamente en desarrollo
- Revisa los logs con emojis para debugging rápido (📥, ✅, ❌)
- Prueba diferentes categorías y montos
- Personaliza las respuestas de la IA según tu audiencia

---

¿Problemas? Abre un issue en GitHub. ¡Buena suerte! 🚀
