# 📐 Arquitectura del Sistema AgroAsistente

## Diagrama de Flujo Completo

```mermaid
graph TB
    subgraph "Usuario"
        A[👤 Agricultor] -->|Mensaje de texto o audio| B[📱 WhatsApp]
    end
    
    subgraph "Capa de Mensajería"
        B --> C[WhatsApp Business API]
        C --> D[🔷 Chatwoot]
    end
    
    subgraph "Backend Personalizado FastAPI"
        D -->|Webhook POST /webhook| E[🎯 Endpoint Principal]
        E --> F{Tipo de mensaje?}
        
        F -->|Texto| G[📝 Procesar Texto]
        F -->|Audio| H[🎤 Descargar Audio]
        
        H --> I[🗣️ Speech-to-Text]
        I -->|Google STT o Whisper| J[Texto transcrito]
        
        G --> K[🤖 Google Gemini AI]
        J --> K
        
        K --> L{Respuesta de IA}
        
        L -->|Tool Call: registrar_gasto| M[💾 BigQuery]
        L -->|Respuesta de texto| N[💬 Enviar mensaje]
        
        M --> O[Generar confirmación]
        O --> N
        
        N --> D
    end
    
    subgraph "Google Cloud"
        M --> P[(📊 BigQuery Database)]
        P --> Q[📈 Looker Studio]
    end
    
    D --> B
    B --> A
    
    style E fill:#4285f4,color:#fff
    style K fill:#ea4335,color:#fff
    style M fill:#34a853,color:#fff
    style Q fill:#fbbc04,color:#000
```

## Diagrama de Secuencia - Flujo de Gasto

```mermaid
sequenceDiagram
    participant U as Agricultor
    participant W as WhatsApp
    participant C as Chatwoot
    participant B as Backend
    participant G as Gemini AI
    participant BQ as BigQuery
    participant L as Looker Studio

    U->>W: "gasté 500 en semillas"
    W->>C: Mensaje entrante
    C->>B: POST /webhook
    
    B->>B: Validar payload
    B->>B: Extraer texto
    
    B->>G: Procesar mensaje
    G->>G: Analizar con IA
    G-->>B: Tool Call: registrar_gasto
    
    B->>BQ: INSERT INTO gastos
    BQ-->>B: Confirmación
    
    B->>B: Generar mensaje
    B->>C: POST /messages
    C->>W: Mensaje saliente
    W->>U: "✅ ¡Gasto registrado!"
    
    Note over L: Dashboard se actualiza automáticamente
```

## Diagrama de Componentes

```mermaid
graph LR
    subgraph "Servicios"
        A[chatwoot.py]
        B[gemini.py]
        C[transcription.py]
        D[bigquery.py]
    end
    
    subgraph "Handler"
        E[webhook.py]
    end
    
    subgraph "Modelos"
        F[schemas.py]
    end
    
    subgraph "Configuración"
        G[config.py]
        H[.env]
    end
    
    E --> A
    E --> B
    E --> C
    E --> D
    
    A --> F
    B --> F
    C --> F
    D --> F
    
    A --> G
    B --> G
    C --> G
    D --> G
    
    G --> H
```

## Estructura de Datos

### Payload de Chatwoot (Entrada)
```json
{
  "event": "message_created",
  "account": {
    "id": 1
  },
  "conversation": {
    "id": 123
  },
  "message_type": "incoming",
  "content": "gasté 500 en semillas",
  "attachments": [
    {
      "id": 456,
      "file_type": "audio/ogg",
      "data_url": "https://..."
    }
  ],
  "sender": {
    "id": 789,
    "phone_number": "+521234567890"
  }
}
```

### Respuesta de Gemini (Tool Call)
```json
{
  "type": "tool_call",
  "data": {
    "monto": 500,
    "categoria": "Semillas 🌱",
    "descripcion": "semillas de jitomate"
  }
}
```

### Registro en BigQuery
```json
{
  "id_gasto": "550e8400-e29b-41d4-a716-446655440000",
  "id_usuario": "+521234567890",
  "fecha": "2025-01-15T10:30:00.000Z",
  "monto": 500.0,
  "categoria": "Semillas 🌱",
  "descripcion": "semillas de jitomate"
}
```

## Flujos de Decisión

### Procesamiento de Mensaje

```mermaid
flowchart TD
    A[Recibir Webhook] --> B{message_type == incoming?}
    B -->|No| C[Ignorar]
    B -->|Sí| D{Tiene content?}
    
    D -->|Sí| E[Usar texto directamente]
    D -->|No| F{Tiene attachments?}
    
    F -->|No| C
    F -->|Sí| G{Es audio?}
    
    G -->|No| H[Enviar error]
    G -->|Sí| I[Descargar audio]
    
    I --> J[Transcribir con STT]
    J --> K[Texto transcrito]
    
    E --> L[Enviar a Gemini]
    K --> L
    
    L --> M{Tipo de respuesta?}
    
    M -->|tool_call| N[Extraer datos]
    M -->|text| O[Obtener mensaje]
    
    N --> P[Insertar en BigQuery]
    P --> Q[Generar confirmación]
    Q --> R[Enviar a Chatwoot]
    
    O --> R
    
    R --> S[Fin]
    H --> S
    C --> S
```

## Tecnologías y Versiones

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Backend | Python | 3.11+ |
| Framework | FastAPI | 0.109.0 |
| IA | Google Gemini | 1.5 Flash |
| STT | Google Speech-to-Text | Latest |
| STT Alt | OpenAI Whisper | whisper-1 |
| Database | BigQuery | Latest |
| Dashboard | Looker Studio | Latest |
| Validación | Pydantic | 2.5.3 |

## Escalabilidad

```mermaid
graph TB
    subgraph "Producción"
        A[Load Balancer] --> B[Backend 1]
        A --> C[Backend 2]
        A --> D[Backend N]
        
        B --> E[BigQuery]
        C --> E
        D --> E
        
        B --> F[Gemini API]
        C --> F
        D --> F
    end
    
    style A fill:#ff6b6b
    style E fill:#4ecdc4
    style F fill:#ffe66d
```

## Seguridad

- ✅ Variables de entorno para secretos
- ✅ Validación de payloads con Pydantic
- ✅ Manejo de excepciones robusto
- ✅ HTTPS en producción
- ⚠️ Recomendado: HMAC signature verification
- ⚠️ Recomendado: Rate limiting

## Performance

- ⚡ Async/await para operaciones I/O
- ⚡ BigQuery streaming inserts
- ⚡ Procesamiento en memoria (no se guarda audio)
- ⚡ Múltiples workers en producción

---

**Última actualización**: Enero 2025
