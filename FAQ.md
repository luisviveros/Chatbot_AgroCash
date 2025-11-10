# ❓ FAQ y Troubleshooting - AgroAsistente

## Preguntas Frecuentes (FAQ)

### 🔧 Instalación y Configuración

#### ¿Qué versión de Python necesito?
Python 3.11 o superior. Verifica con:
```bash
python --version
```

#### ¿Dónde consigo las API keys?
- **Gemini**: https://ai.google.dev/ (gratuito con límites)
- **Chatwoot**: Settings → Applications → API Access Tokens
- **OpenAI** (opcional): https://platform.openai.com/api-keys

#### ¿Necesito una cuenta de Google Cloud?
Sí, para:
- BigQuery (almacenamiento de datos)
- Speech-to-Text (transcripción de audio, opcional)

Puedes empezar con el free tier de GCP.

#### ¿Cuánto cuesta ejecutar esto?
**Costos aproximados por mes** (uso moderado):
- BigQuery: $0-5 (free tier cubre la mayoría)
- Gemini: Gratis hasta 60 requests/minuto
- Speech-to-Text: $0.006 por 15 segundos (o usa Whisper)
- Cloud Run: $0-10 (free tier incluye bastante)

**Total estimado**: $0-15/mes para uso pequeño/mediano

---

### 🚀 Uso y Funcionalidad

#### ¿El bot entiende español?
Sí, está completamente configurado para español de México, pero funciona con cualquier variante del español.

#### ¿Puedo cambiar las categorías?
Sí, edita el archivo `app/services/gemini.py`:
```python
"enum": [
    "Tu Categoría 1",
    "Tu Categoría 2",
    # ... más categorías
]
```

#### ¿Funciona con otros idiomas?
Sí, solo cambia:
1. El `SYSTEM_PROMPT` en `gemini.py`
2. El parámetro `language_code` en `transcription.py`

#### ¿Puedo usar otro modelo de IA?
Sí, puedes reemplazar Gemini con:
- OpenAI GPT-4 (requiere adaptar el código de function calling)
- Claude (similar)
- Llama (local)

#### ¿Puedo conectar múltiples números de WhatsApp?
Sí, cada número tendrá su propio `id_usuario` en BigQuery. Solo asegúrate de configurar los webhooks para cada inbox en Chatwoot.

---

### 📊 Datos y Dashboard

#### ¿Cómo conecto Looker Studio?
1. Crea un nuevo reporte en https://lookerstudio.google.com
2. Conecta BigQuery como fuente de datos
3. Selecciona tu tabla `agrocash.gastos`
4. Crea visualizaciones

#### ¿Puedo exportar mis datos?
Sí, desde BigQuery:
```sql
SELECT * FROM agrocash.gastos
WHERE id_usuario = '+521234567890'
```
Exporta como CSV, JSON, o Parquet.

#### ¿Los datos están seguros?
Sí:
- BigQuery está encriptado en reposo y en tránsito
- Solo tú tienes acceso con tus credenciales de GCP
- Sigue las mejores prácticas de seguridad

---

## 🐛 Troubleshooting

### Problemas de Instalación

#### Error: `pip install` falla

**Síntoma:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solución:**
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar con verbose para ver el error
pip install -r requirements.txt -v
```

#### Error: `No module named 'app'`

**Síntoma:**
```
ModuleNotFoundError: No module named 'app'
```

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd agroasistente-backend

# Ejecuta desde la raíz del proyecto
python app/main.py
```

---

### Problemas con Variables de Entorno

#### Error: `Field required`

**Síntoma:**
```
pydantic_core._pydantic_core.ValidationError: 
Field required [type=missing]
```

**Solución:**
```bash
# Verifica que el archivo .env existe
ls -la .env

# Verifica que todas las variables requeridas están presentes
cat .env

# Asegúrate de que no hay espacios alrededor del =
# ✅ Correcto:   GEMINI_API_KEY=abc123
# ❌ Incorrecto: GEMINI_API_KEY = abc123
```

#### El sistema no lee el archivo .env

**Solución:**
```bash
# Exporta las variables manualmente (temporal)
export GEMINI_API_KEY="tu-key"
export CHATWOOT_API_KEY="tu-key"
# ... etc

# O carga el .env explícitamente
source .env
python app/main.py
```

---

### Problemas con Google Cloud

#### Error: `DefaultCredentialsError`

**Síntoma:**
```
google.auth.exceptions.DefaultCredentialsError: 
Could not automatically determine credentials
```

**Solución:**
```bash
# Opción 1: Variable de entorno
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Opción 2: Configurar en .env
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/service-account.json

# Verifica que el archivo existe
ls -la /path/to/key.json
```

#### Error: `PermissionDenied` en BigQuery

**Síntoma:**
```
google.api_core.exceptions.PermissionDenied: 
403 Access Denied: BigQuery
```

**Solución:**
1. Ve a Google Cloud Console
2. IAM & Admin → Service Accounts
3. Encuentra tu service account
4. Agrega roles:
   - BigQuery Data Editor
   - BigQuery User

#### La tabla no se crea automáticamente

**Solución:**
```bash
# Ejecuta manualmente
python -c "from app.services.bigquery import bigquery_service; bigquery_service.create_table_if_not_exists()"
```

---

### Problemas con Gemini

#### Error: `Invalid API key`

**Síntoma:**
```
google.api_core.exceptions.PermissionDenied: 
400 API key not valid
```

**Solución:**
1. Verifica tu API key en https://ai.google.dev/
2. Asegúrate de copiarla correctamente (sin espacios)
3. Verifica que no haya expirado

#### Error: `Resource exhausted`

**Síntoma:**
```
google.api_core.exceptions.ResourceExhausted: 
429 Quota exceeded
```

**Solución:**
1. Has excedido el límite gratuito (60 req/min)
2. Espera un minuto y prueba de nuevo
3. Considera actualizar a un plan de pago

#### La IA no extrae los datos correctamente

**Solución:**
1. Revisa el `SYSTEM_PROMPT` en `app/services/gemini.py`
2. Asegúrate de que las categorías sean claras
3. Prueba con mensajes más explícitos
4. Revisa los logs para ver qué envía Gemini

---

### Problemas con Transcripción

#### Error: `Speech-to-Text API not enabled`

**Síntoma:**
```
google.api_core.exceptions.PermissionDenied: 
Speech-to-Text API has not been used
```

**Solución:**
1. Ve a https://console.cloud.google.com
2. Busca "Speech-to-Text API"
3. Haz clic en "Enable"

#### La transcripción es imprecisa

**Solución:**
```python
# Cambia el modelo en transcription.py
config = speech.RecognitionConfig(
    encoding=encoding,
    language_code="es-MX",
    model="command_and_search",  # Mejor para comandos cortos
    use_enhanced=True  # Modelo mejorado
)
```

#### Prefiero usar Whisper en lugar de Google STT

**Solución:**
```bash
# En .env
STT_PROVIDER=openai
OPENAI_API_KEY=tu-key-de-openai
```

---

### Problemas con Chatwoot

#### No recibo webhooks

**Síntoma:**
El endpoint `/webhook` nunca recibe peticiones.

**Solución:**
1. Verifica que el servidor esté corriendo:
   ```bash
   curl http://localhost:8000/health
   ```

2. Si usas ngrok, verifica que esté activo:
   ```bash
   ngrok http 8000
   ```

3. En Chatwoot:
   - Settings → Webhooks
   - Verifica que la URL sea correcta
   - Asegúrate de que "Message Created" esté marcado
   - El webhook debe estar "Enabled"

4. Revisa los logs de Chatwoot para errores

#### Error: `Failed to send message to Chatwoot`

**Síntoma:**
```
httpx.HTTPStatusError: 401 Unauthorized
```

**Solución:**
1. Verifica tu `CHATWOOT_API_KEY`
2. Asegúrate de que sea un "API Access Token", no un "Agent Bot Token"
3. Verifica que la URL base sea correcta (sin `/` al final)

---

### Problemas de Rendimiento

#### El sistema es lento

**Causas comunes:**
1. Red lenta → La transcripción de audio toma tiempo
2. Gemini responde lento → Puede tardar 2-5 segundos
3. Procesamiento de audio grande → Limita el tamaño de archivos

**Soluciones:**
```python
# En main.py, aumenta workers
uvicorn app.main:app --workers 4

# Configura timeouts más largos
# En chatwoot.py y transcription.py
async with httpx.AsyncClient(timeout=60.0) as client:
```

#### Muchas peticiones simultáneas fallan

**Solución:**
```bash
# Aumenta workers
uvicorn app.main:app --workers 8

# O usa gunicorn
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --workers 4
```

---

### Problemas de Producción

#### El servidor se cae frecuentemente

**Solución:**
```bash
# Usa un process manager
pip install supervisor

# O despliega en Cloud Run que maneja esto automáticamente
gcloud run deploy agroasistente-backend --source .
```

#### Los logs son difíciles de leer

**Solución:**
```python
# Agrega logging estructurado en main.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### No puedo hacer debug

**Solución:**
```bash
# Ejecuta con reload y debug
uvicorn app.main:app --reload --log-level debug

# O usa pdb
import pdb; pdb.set_trace()
```

---

## 🔍 Comandos Útiles de Diagnóstico

### Verificar Conexiones

```bash
# Probar BigQuery
python -c "
from app.services.bigquery import bigquery_service
print('BigQuery OK')
"

# Probar Gemini
python -c "
from app.services.gemini import gemini_service
import asyncio
result = asyncio.run(gemini_service.process_message('hola'))
print(result)
"

# Probar Chatwoot
curl -H "api_access_token: tu-key" \
  https://app.chatwoot.com/api/v1/accounts
```

### Ver Logs en Tiempo Real

```bash
# Si desplegaste en Cloud Run
gcloud run logs tail agroasistente-backend

# Local con uvicorn
uvicorn app.main:app --log-level debug
```

### Limpiar y Reiniciar

```bash
# Borrar cache de Python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 📞 ¿Aún tienes problemas?

1. **Revisa los logs**: La mayoría de errores están ahí
2. **Consulta la documentación**: [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Prueba con curl**: Envía requests directos al endpoint
4. **Simplifica**: Prueba cada componente por separado
5. **Abre un issue**: En GitHub con logs y pasos para reproducir

---

## 💡 Tips Pro para Debug

```python
# En webhook.py, agrega logs detallados
print(f"📥 Payload completo: {json.dumps(payload_dict, indent=2)}")

# Guarda payloads para análisis
with open(f"payload_{datetime.now()}.json", "w") as f:
    json.dump(payload_dict, f, indent=2)

# Simula respuestas de Gemini
# Comenta la llamada real y usa un dict hardcodeado
gemini_response = {
    "type": "tool_call",
    "data": {"monto": 500, "categoria": "Semillas 🌱"}
}
```

---

**Última actualización**: Enero 2025
