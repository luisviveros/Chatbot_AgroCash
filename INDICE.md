# 🗺️ Índice de Navegación - AgroAsistente Backend

## 🚀 Empieza Aquí

¿Nuevo en el proyecto? Sigue este orden:

1. 📋 **[RESUMEN.md](RESUMEN.md)** - Visión general del proyecto (5 min)
2. ⚡ **[QUICKSTART.md](QUICKSTART.md)** - Setup rápido paso a paso (15-30 min)
3. 📖 **[README.md](README.md)** - Documentación completa (30 min)

---

## 📚 Documentación por Caso de Uso

### 🎯 "Quiero entender qué hace el sistema"
→ **[RESUMEN.md](RESUMEN.md)** - Resumen ejecutivo con ejemplos

### ⚡ "Quiero ponerlo a funcionar YA"
→ **[QUICKSTART.md](QUICKSTART.md)** - Guía de inicio rápido

### 📖 "Necesito la documentación completa"
→ **[README.md](README.md)** - Manual completo con todos los detalles

### 🏗️ "Quiero entender la arquitectura"
→ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diagramas y diseño del sistema

### 💡 "Quiero ver ejemplos de uso"
→ **[EXAMPLES.md](EXAMPLES.md)** - Casos de uso reales con código

### ❓ "Tengo un problema o pregunta"
→ **[FAQ.md](FAQ.md)** - Preguntas frecuentes y troubleshooting

### 🚀 "Quiero desplegarlo a producción"
→ **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía de deployment completa

---

## 📂 Navegación por Archivos

### Documentación (Markdown)

| Archivo | Propósito | Tiempo de Lectura |
|---------|-----------|-------------------|
| [RESUMEN.md](RESUMEN.md) | Visión general ejecutiva | 5 min |
| [QUICKSTART.md](QUICKSTART.md) | Setup rápido | 15-30 min |
| [README.md](README.md) | Documentación completa | 30 min |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Diseño técnico | 20 min |
| [EXAMPLES.md](EXAMPLES.md) | Casos de uso | 15 min |
| [FAQ.md](FAQ.md) | Troubleshooting | Variable |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guía de producción | 30 min |

### Código Python

| Archivo | Qué Hace | Cuándo Modificar |
|---------|----------|------------------|
| `app/main.py` | Punto de entrada FastAPI | Setup inicial |
| `app/config.py` | Configuración del sistema | Agregar variables |
| `app/models/schemas.py` | Modelos de datos | Cambiar estructura |
| `app/services/chatwoot.py` | Cliente Chatwoot | Customizar mensajes |
| `app/services/gemini.py` | IA y Function Calling | Cambiar categorías |
| `app/services/transcription.py` | Speech-to-Text | Cambiar proveedor |
| `app/services/bigquery.py` | Base de datos | Modificar schema |
| `app/handlers/webhook.py` | Lógica principal | Cambiar flujo |

### Configuración

| Archivo | Propósito |
|---------|-----------|
| `.env.example` | Template de variables de entorno |
| `requirements.txt` | Dependencias Python |
| `.gitignore` | Archivos ignorados por Git |

### Testing

| Archivo | Propósito |
|---------|-----------|
| `test_webhook.py` | Tests automatizados del webhook |

---

## 🔍 Búsqueda Rápida por Tema

### Instalación y Setup
- [Requisitos del Sistema](README.md#-instalación)
- [Variables de Entorno](QUICKSTART.md#2️⃣-configurar-variables-de-entorno-10-minutos)
- [Guía Paso a Paso](QUICKSTART.md)

### Configuración
- [Chatwoot Setup](README.md#-configurar-webhook-en-chatwoot)
- [Google Cloud Setup](QUICKSTART.md#3️⃣-crear-dataset-en-bigquery-2-minutos)
- [API Keys](QUICKSTART.md#lo-que-necesitas)

### Desarrollo
- [Estructura del Código](README.md#-arquitectura-del-proyecto)
- [Modelos de Datos](ARCHITECTURE.md#estructura-de-datos)
- [Flujo del Sistema](ARCHITECTURE.md#diagrama-de-secuencia---flujo-de-gasto)

### IA y Procesamiento
- [System Prompt](app/services/gemini.py#L14-L31)
- [Categorías](RESUMEN.md#-categorías-de-gastos)
- [Function Calling](ARCHITECTURE.md#respuesta-de-gemini-tool-call)

### Testing
- [Pruebas Locales](QUICKSTART.md#5️⃣-probar-localmente-2-minutos)
- [Script de Tests](test_webhook.py)
- [Ejemplos de Uso](EXAMPLES.md)

### Deployment
- [Cloud Run](DEPLOYMENT.md#1-google-cloud-run-recomendado-)
- [Docker](DEPLOYMENT.md#2-docker--vm)
- [Kubernetes](DEPLOYMENT.md#3-kubernetes-para-alta-escala)

### Troubleshooting
- [Problemas Comunes](FAQ.md#-troubleshooting)
- [Error de Instalación](FAQ.md#problemas-de-instalación)
- [Error de Producción](FAQ.md#problemas-de-producción)

### Costos
- [Estimación Mensual](RESUMEN.md#-costos-estimados)
- [Breakdown Detallado](DEPLOYMENT.md#-estimación-de-costos-mensuales)

---

## 🎯 Flujos de Trabajo Comunes

### 🆕 Primer Setup (Usuario Nuevo)

```
1. RESUMEN.md (entender el proyecto)
   ↓
2. QUICKSTART.md (setup en 30 min)
   ↓
3. test_webhook.py (probar localmente)
   ↓
4. EXAMPLES.md (ver casos de uso)
   ↓
5. README.md (profundizar)
```

### 🔧 Desarrollo y Customización

```
1. README.md (entender arquitectura)
   ↓
2. ARCHITECTURE.md (ver diagramas)
   ↓
3. Modificar código en app/
   ↓
4. test_webhook.py (validar cambios)
   ↓
5. FAQ.md (resolver problemas)
```

### 🚀 Deployment a Producción

```
1. DEPLOYMENT.md (elegir estrategia)
   ↓
2. Configurar variables de entorno
   ↓
3. Seguir guía de deployment
   ↓
4. Configurar monitoreo
   ↓
5. Smoke tests
```

### 🐛 Debugging y Soporte

```
1. FAQ.md (buscar problema)
   ↓
2. Ver logs del sistema
   ↓
3. test_webhook.py (reproducir)
   ↓
4. ARCHITECTURE.md (entender flujo)
   ↓
5. Abrir issue en GitHub
```

---

## 🔗 Enlaces Externos Útiles

### APIs y Servicios
- [Chatwoot API Docs](https://www.chatwoot.com/developers/api/)
- [Google Gemini](https://ai.google.dev/)
- [BigQuery Docs](https://cloud.google.com/bigquery/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Tutoriales
- [Function Calling con Gemini](https://ai.google.dev/docs/function_calling)
- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts)
- [Looker Studio](https://lookerstudio.google.com/)

### Herramientas
- [ngrok](https://ngrok.com/) - Túneles para desarrollo
- [Postman](https://www.postman.com/) - Testing de APIs
- [Docker Hub](https://hub.docker.com/) - Registro de imágenes

---

## 📊 Mapeo: Problema → Solución

| Problema | Documento | Sección |
|----------|-----------|---------|
| No sé por dónde empezar | QUICKSTART.md | Todo |
| Error al instalar | FAQ.md | Instalación |
| Webhook no funciona | FAQ.md | Chatwoot |
| IA no extrae datos | FAQ.md | Gemini |
| Quiero cambiar categorías | README.md | Categorías |
| Cómo desplegar | DEPLOYMENT.md | Todo |
| Necesito ejemplos | EXAMPLES.md | Todo |
| Entender arquitectura | ARCHITECTURE.md | Diagramas |
| Costos mensuales | RESUMEN.md | Costos |
| Testing | test_webhook.py | - |

---

## 🎓 Nivel de Experiencia Recomendado

### Para Empezar
- ✅ Python básico
- ✅ APIs REST
- ✅ Variables de entorno
- ✅ Línea de comandos

### Para Customizar
- ✅ Python intermedio
- ✅ FastAPI
- ✅ Async/await
- ✅ Google Cloud básico

### Para Producción
- ✅ DevOps básico
- ✅ Docker
- ✅ Cloud deployment
- ✅ Monitoreo

---

## ✅ Checklist de Navegación

Marca lo que ya leíste:

### Básico
- [ ] RESUMEN.md
- [ ] QUICKSTART.md
- [ ] README.md

### Intermedio
- [ ] ARCHITECTURE.md
- [ ] EXAMPLES.md
- [ ] test_webhook.py

### Avanzado
- [ ] FAQ.md
- [ ] DEPLOYMENT.md
- [ ] Código fuente completo

---

## 🆘 ¿Perdido?

Si no sabes qué leer:

1. **Completo novato**: Empieza con [RESUMEN.md](RESUMEN.md)
2. **Quiero usarlo ya**: Ve a [QUICKSTART.md](QUICKSTART.md)
3. **Soy desarrollador**: Lee [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Tengo un error**: Busca en [FAQ.md](FAQ.md)
5. **Voy a producción**: Sigue [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📝 Notas

- Todos los archivos .md están escritos en español
- El código tiene comentarios en español
- La documentación está diseñada para ser leída en orden
- Cada documento es autocontenido pero se complementan

---

**Tip**: Usa el buscador de tu editor (Ctrl+F / Cmd+F) para encontrar términos específicos en los documentos.

**Última actualización**: Enero 2025
