# 🚀 Guía de Deployment - AgroAsistente

## Opciones de Deployment

### 1. Google Cloud Run (Recomendado) ⭐

**Ventajas:**
- ✅ Serverless (no administrar servidores)
- ✅ Auto-scaling automático
- ✅ Solo pagas por uso
- ✅ HTTPS automático
- ✅ Integración nativa con GCP

**Pasos:**

#### a) Preparar el Proyecto

```bash
# Crear Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app ./app

# Puerto que Cloud Run espera
ENV PORT=8080
EXPOSE 8080

# Comando de inicio
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF
```

#### b) Crear .dockerignore

```bash
cat > .dockerignore << 'EOF'
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.env.local
*.log
.git
.gitignore
README.md
*.md
test_*.py
EOF
```

#### c) Configurar Variables de Entorno en Cloud Run

```bash
# Opción 1: Usando archivo de secretos
gcloud secrets create agroasistente-secrets --data-file=.env

# Opción 2: Una por una
gcloud secrets create gemini-api-key --data-file=-
# Pega tu key y presiona Ctrl+D
```

#### d) Deploy

```bash
# Authenticate
gcloud auth login
gcloud config set project TU-PROJECT-ID

# Deploy
gcloud run deploy agroasistente-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars CHATWOOT_BASE_URL=https://app.chatwoot.com \
  --set-secrets CHATWOOT_API_KEY=chatwoot-api-key:latest \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --set-secrets OPENAI_API_KEY=openai-api-key:latest \
  --set-env-vars GCP_PROJECT_ID=TU-PROJECT-ID \
  --set-env-vars BIGQUERY_DATASET=agrocash \
  --set-env-vars BIGQUERY_TABLE=gastos \
  --set-env-vars STT_PROVIDER=google \
  --set-env-vars DASHBOARD_URL=https://lookerstudio.google.com/... \
  --memory 1Gi \
  --cpu 1 \
  --timeout 60s \
  --max-instances 10
```

#### e) Obtener URL

```bash
# Ver la URL del servicio
gcloud run services describe agroasistente-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

---

### 2. Docker + VM

**Para tener más control:**

#### a) Construir Imagen

```bash
docker build -t agroasistente-backend .
```

#### b) Probar Localmente

```bash
docker run -p 8000:8000 \
  --env-file .env \
  agroasistente-backend
```

#### c) Subir a Docker Hub

```bash
docker tag agroasistente-backend tu-usuario/agroasistente-backend:latest
docker push tu-usuario/agroasistente-backend:latest
```

#### d) Desplegar en VM

```bash
# En tu VM (DigitalOcean, AWS, GCP)
docker pull tu-usuario/agroasistente-backend:latest

docker run -d \
  --name agroasistente \
  --restart always \
  -p 80:8000 \
  --env-file .env \
  tu-usuario/agroasistente-backend:latest
```

---

### 3. Kubernetes (Para Alta Escala)

#### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agroasistente-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agroasistente
  template:
    metadata:
      labels:
        app: agroasistente
    spec:
      containers:
      - name: backend
        image: tu-usuario/agroasistente-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: CHATWOOT_API_KEY
          valueFrom:
            secretKeyRef:
              name: agroasistente-secrets
              key: chatwoot-api-key
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: agroasistente-secrets
              key: gemini-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: agroasistente-service
spec:
  selector:
    app: agroasistente
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
```

---

## 🔒 Seguridad en Producción

### 1. Verificar Webhooks con HMAC

Agrega verificación de firma en `app/main.py`:

```python
import hmac
import hashlib

WEBHOOK_SECRET = os.getenv("CHATWOOT_WEBHOOK_SECRET")

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verifica la firma HMAC del webhook"""
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@app.post("/webhook")
async def webhook_endpoint(request: Request):
    # Obtener payload raw
    body = await request.body()
    
    # Verificar firma
    signature = request.headers.get("X-Chatwoot-Signature")
    if not verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Continuar procesamiento...
```

### 2. Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/webhook")
@limiter.limit("100/minute")
async def webhook_endpoint(request: Request):
    ...
```

### 3. CORS (Si necesitas frontend)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoreo y Logging

### 1. Google Cloud Logging

```python
from google.cloud import logging as cloud_logging

logging_client = cloud_logging.Client()
logging_client.setup_logging()

import logging
logger = logging.getLogger(__name__)

logger.info("Mensaje de log", extra={
    "labels": {
        "user_id": user_id,
        "environment": "production"
    }
})
```

### 2. Prometheus + Grafana

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
```

### 3. Sentry (Monitoreo de Errores)

```bash
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="tu-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

---

## 🔧 Configuración de Nginx (Si usas VM)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Para webhooks largos
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}
```

```bash
# Obtener certificado SSL gratis
sudo certbot --nginx -d tu-dominio.com
```

---

## 🔄 CI/CD con GitHub Actions

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build
      run: |
        docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/agroasistente-backend .
        docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/agroasistente-backend
    
    - name: Deploy
      run: |
        gcloud run deploy agroasistente-backend \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/agroasistente-backend \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
```

---

## 📈 Optimización de Performance

### 1. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_category_mapping():
    """Cache de categorías"""
    return {...}
```

### 2. Connection Pooling

```python
# Para BigQuery
from google.cloud import bigquery

client = bigquery.Client(
    project=project_id,
    client_options={"api_endpoint": "bigquery.googleapis.com"},
)
```

### 3. Async Everything

```python
import aiofiles

async def save_audio_temp(audio_bytes):
    async with aiofiles.open("temp.ogg", "wb") as f:
        await f.write(audio_bytes)
```

---

## 🧪 Testing en Producción

### 1. Health Checks

```python
@app.get("/health")
async def health_check():
    checks = {
        "bigquery": await check_bigquery(),
        "gemini": await check_gemini(),
        "chatwoot": await check_chatwoot()
    }
    
    if all(checks.values()):
        return {"status": "healthy", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail=checks)
```

### 2. Smoke Tests Post-Deploy

```bash
#!/bin/bash
# smoke_test.sh

URL="https://tu-dominio.com"

# Test health
curl -f $URL/health || exit 1

# Test webhook con datos dummy
curl -f -X POST $URL/webhook \
  -H "Content-Type: application/json" \
  -d '{"message_type":"outgoing"}' || exit 1

echo "✅ Smoke tests passed"
```

---

## 📋 Checklist Pre-Producción

- [ ] Variables de entorno configuradas
- [ ] Certificado SSL activo (HTTPS)
- [ ] Webhooks de Chatwoot apuntando a producción
- [ ] BigQuery dataset y tabla creados
- [ ] Service Account con permisos correctos
- [ ] Rate limiting configurado
- [ ] Logging y monitoreo activos
- [ ] Backups de base de datos programados
- [ ] Alertas de errores configuradas (Sentry)
- [ ] Documentación de runbook para el equipo
- [ ] Plan de rollback definido

---

## 🔥 Plan de Rollback

Si algo sale mal:

```bash
# Cloud Run - volver a versión anterior
gcloud run services update-traffic agroasistente-backend \
  --to-revisions=PREVIOUS_REVISION=100

# Docker - usar imagen anterior
docker pull tu-usuario/agroasistente-backend:previous
docker stop agroasistente
docker rm agroasistente
docker run -d --name agroasistente ... :previous

# Verificar
curl https://tu-dominio.com/health
```

---

## 📞 Soporte Post-Deploy

### Monitorear Logs

```bash
# Cloud Run
gcloud run logs tail agroasistente-backend --format=json

# Docker
docker logs -f agroasistente

# Filtrar errores
gcloud run logs read agroasistente-backend --filter="severity=ERROR"
```

### Dashboard de Métricas

En Google Cloud Console:
1. Monitoring → Dashboards
2. Crea dashboard con:
   - Request count
   - Latency
   - Error rate
   - BigQuery inserts
   - Gemini API calls

---

## 💰 Estimación de Costos Mensuales

Para **1000 usuarios activos**, ~10 mensajes/día:

| Servicio | Costo Mensual |
|----------|---------------|
| Cloud Run | $10-30 |
| BigQuery | $5-15 |
| Gemini API | $0 (free tier) |
| Speech-to-Text | $10-20 |
| Egress (salida) | $5-10 |
| **Total** | **$30-75** |

Para escalar a 10,000 usuarios: ~$200-400/mes

---

¿Listo para production? ¡Adelante! 🚀
