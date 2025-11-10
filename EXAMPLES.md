# 💡 Ejemplos de Uso - AgroAsistente

## Casos de Uso Reales

### 1. Registrar Gastos Simples

#### Entrada del Usuario:
```
"gasté 500 en semillas"
```

#### Procesamiento:
- ✅ Gemini detecta: gasto de $500
- ✅ Categoría inferida: "Semillas 🌱"
- ✅ Se registra en BigQuery

#### Respuesta del Bot:
```
✅ ¡Gasto registrado!

💰 Monto: $500.00
📂 Categoría: Semillas 🌱

🔍 ID: 550e8400...
```

---

### 2. Registrar Gastos con Detalles

#### Entrada del Usuario:
```
"compré fertilizante NPK 18-46-0 por 2,500 pesos"
```

#### Procesamiento:
- ✅ Monto: $2,500
- ✅ Categoría: "Fertilizantes 🧪"
- ✅ Descripción: "fertilizante NPK 18-46-0"

#### Respuesta del Bot:
```
✅ ¡Gasto registrado!

💰 Monto: $2,500.00
📂 Categoría: Fertilizantes 🧪
📝 Descripción: fertilizante NPK 18-46-0

🔍 ID: a1b2c3d4...
```

---

### 3. Registrar Ingresos

#### Entrada del Usuario:
```
"vendí 2 toneladas de jitomate por 35,000"
```

#### Procesamiento:
- ✅ Monto: $35,000
- ✅ Categoría: "Ingresos 💰"
- ✅ Descripción: "2 toneladas de jitomate"

#### Respuesta del Bot:
```
✅ ¡Gasto registrado!

💰 Monto: $35,000.00
📂 Categoría: Ingresos 💰
📝 Descripción: 2 toneladas de jitomate

🔍 ID: f9e8d7c6...
```

---

### 4. Saludos y Conversación

#### Entrada del Usuario:
```
"Hola"
```

#### Respuesta del Bot:
```
¡Hola! Para ayudarte a ahorrar, puedo registrar tus ingresos y gastos. 
¿Tienes algún movimiento que te gustaría anotar?
```

---

### 5. Solicitar Dashboard

#### Entrada del Usuario:
```
"quiero ver el reporte"
```

#### Respuesta del Bot:
```
¡Claro! Aquí puedes ver el resumen de todos tus movimientos en el dashboard:
https://lookerstudio.google.com/reporting/906bb9db-7a23-480f-8825-09148ceefce6
```

---

### 6. Mensajes de Voz (Audio)

#### Entrada del Usuario:
🎤 **Audio**: "Pagué tres mil pesos de mano de obra para la cosecha"

#### Procesamiento:
1. 🎤 Se descarga el audio
2. 🗣️ Se transcribe: "Pagué tres mil pesos de mano de obra para la cosecha"
3. 🤖 Gemini procesa el texto
4. ✅ Se registra en BigQuery

#### Respuesta del Bot:
```
✅ ¡Gasto registrado!

💰 Monto: $3,000.00
📂 Categoría: Mano de Obra 🧑‍🌾
📝 Descripción: para la cosecha

🔍 ID: 1a2b3c4d...
```

---

## Variaciones de Lenguaje Natural

El sistema entiende múltiples formas de expresar lo mismo:

### Para Gastos:
- "gasté 500 en semillas"
- "compré semillas por 500"
- "pagué 500 de semillas"
- "me costó 500 de semillas"
- "invertí 500 en semillas"

### Para Ingresos:
- "vendí por 10000"
- "ingresé 10000"
- "gané 10000 con la venta"
- "me pagaron 10000"
- "cobré 10000"

### Para Dashboard:
- "quiero ver el reporte"
- "muéstrame el dashboard"
- "ya terminé"
- "eso es todo"
- "quiero ver mis gastos"

---

## Categorías Disponibles

### 🌱 Semillas
**Ejemplos:**
- "gasté 800 en semillas de maíz"
- "compré semilla de jitomate por 1500"

### 🧪 Fertilizantes
**Ejemplos:**
- "pagué 3000 de fertilizante"
- "compré urea por 2500"

### 💧 Agroquímicos
**Ejemplos:**
- "gasté 1200 en herbicida"
- "compré insecticida por 900"

### 🛠️ Servicios
**Ejemplos:**
- "pagué 5000 por el riego"
- "servicio de tractor 2000"

### 🧑‍🌾 Mano de Obra
**Ejemplos:**
- "pagué 3000 de mano de obra"
- "jornaleros 4500"

### 🚜 Maquinaria
**Ejemplos:**
- "compré un tractor por 150000"
- "reparación del tractor 8000"

### 🚚 Transporte
**Ejemplos:**
- "flete 2500"
- "gasté 1800 en transporte"

### 📦 Empaque
**Ejemplos:**
- "compré cajas por 1500"
- "material de empaque 800"

### 🏠 Rentas
**Ejemplos:**
- "pagué 10000 de renta del terreno"
- "renta 5000"

### 🏗️ Infraestructura
**Ejemplos:**
- "construí un invernadero por 50000"
- "reparación de cerca 3500"

### 💰 Ingresos
**Ejemplos:**
- "vendí la cosecha por 45000"
- "ingreso de 20000 por venta"

---

## Flujos de Conversación Completos

### Escenario 1: Agricultor Registrando Gastos Diarios

```
Usuario: "Hola"
Bot: "¡Hola! Para ayudarte a ahorrar, puedo registrar tus ingresos y 
      gastos. ¿Tienes algún movimiento que te gustaría anotar?"

Usuario: "gasté 500 en semillas de calabaza"
Bot: "✅ ¡Gasto registrado!
      💰 Monto: $500.00
      📂 Categoría: Semillas 🌱
      📝 Descripción: semillas de calabaza"

Usuario: "también compré fertilizante por 2300"
Bot: "✅ ¡Gasto registrado!
      💰 Monto: $2,300.00
      📂 Categoría: Fertilizantes 🧪"

Usuario: "gracias, ya terminé"
Bot: "¡Claro! Aquí puedes ver el resumen de todos tus movimientos:
      https://lookerstudio.google.com/reporting/..."
```

---

### Escenario 2: Registro con Notas de Voz

```
Usuario: 🎤 [Audio]: "Buenos días, quiero registrar que ayer gasté 
         cuatro mil pesos en fertilizante orgánico"

Bot: "✅ ¡Gasto registrado!
      💰 Monto: $4,000.00
      📂 Categoría: Fertilizantes 🧪
      📝 Descripción: fertilizante orgánico"

Usuario: 🎤 [Audio]: "Y también vendí la cosecha de maíz por 
         treinta y cinco mil pesos"

Bot: "✅ ¡Gasto registrado!
      💰 Monto: $35,000.00
      📂 Categoría: Ingresos 💰
      📝 Descripción: cosecha de maíz"
```

---

### Escenario 3: Consulta de Dashboard

```
Usuario: "quiero ver mis gastos del mes"
Bot: "¡Claro! Aquí puedes ver el resumen de todos tus movimientos:
      https://lookerstudio.google.com/reporting/..."

Usuario: "gracias"
Bot: "¡Un placer! ¿Hay algo más que quieras registrar?"
```

---

## Casos Especiales

### ❌ Mensajes sin Información Financiera

#### Entrada:
```
"¿cómo está el clima?"
```

#### Respuesta:
```
Para ayudarte a ahorrar, puedo registrar tus ingresos y gastos. 
¿Tienes algún movimiento que te gustaría anotar?
```

---

### ❌ Archivos No Soportados

#### Entrada:
📷 [Imagen]

#### Respuesta:
```
⚠️ Solo puedo procesar mensajes de texto y notas de voz.
```

---

## Formatos de Número Aceptados

El sistema entiende diferentes formas de escribir números:

- `500` → $500.00
- `1,500` → $1,500.00
- `1500` → $1,500.00
- `10000` → $10,000.00
- `10,000` → $10,000.00
- `2.5` → $2.50
- `mil` → $1,000.00
- `dos mil` → $2,000.00
- `3000 pesos` → $3,000.00

---

## Tips para Mejores Resultados

### ✅ Buenas Prácticas

1. **Sé específico**: "gasté 500 en semillas de jitomate" es mejor que "gasté 500"
2. **Incluye contexto**: "compré fertilizante NPK por 2500" ayuda a la categorización
3. **Usa números claros**: "1500" o "mil quinientos" funcionan bien
4. **Habla natural**: El sistema entiende lenguaje cotidiano

### ❌ Evita

1. Mensajes ambiguos sin montos
2. Múltiples gastos en un solo mensaje (sepáralos)
3. Archivos que no sean audio

---

## Integración con Looker Studio

Una vez registrados los gastos e ingresos, tu dashboard mostrará:

- 📊 Gráficos de gastos por categoría
- 📈 Tendencias mensuales
- 💰 Balance de ingresos vs gastos
- 📅 Historial completo
- 🎯 Análisis de rentabilidad

**Acceso al Dashboard:**
El link se proporciona automáticamente cuando el usuario lo solicita.

---

## Próximas Funcionalidades (Roadmap)

- [ ] Recordatorios de gastos recurrentes
- [ ] Análisis predictivo de costos
- [ ] Alertas de presupuesto
- [ ] Exportación de reportes en PDF
- [ ] Multi-usuario (cooperativas)
- [ ] Integración con bancos

---

**¿Tienes más preguntas?** Revisa el [README.md](README.md) o el [QUICKSTART.md](QUICKSTART.md)
