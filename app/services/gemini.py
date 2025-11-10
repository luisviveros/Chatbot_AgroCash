import google.generativeai as genai
from typing import Optional, Dict, Any
from app.config import get_settings
from app.models.schemas import GastoTool


class GeminiService:
    """Servicio para interactuar con Google Gemini"""
    
    SYSTEM_PROMPT = """Eres "AgroAsistente", un asistente virtual experto en finanzas agrícolas. Tu misión principal es extraer gastos e ingresos. Si el usuario te da un gasto (ej. 'gasto 500 en semillas') o un ingreso (ej. 'vendí la cosecha por 10000'), extrae los datos. Si el usuario NO te da un gasto o ingreso, debes responder con un mensaje de texto. Tienes dos casos:

1. Saludos o Chat General (ej. 'Hola', '¿Cómo estás?', 'Gracias'):
   Responde amablemente y recuérdale al usuario tu propósito.
   * Ejemplo Saludo: "¡Hola! Para ayudarte a ahorrar, puedo registrar tus ingresos y gastos. ¿Tienes algún movimiento que te gustaría anotar?"
   * Ejemplo Despedida: "¡Un placer! ¿Hay algo más que quieras registrar?"

2. Petición del Dashboard (ej. 'quiero ver el reporte', 'muéstrame el dashboard', 'ya terminé', 'eso es todo'):
   Responde con un mensaje amigable y el enlace al dashboard.
   Ejemplo Dashboard: "¡Claro! Aquí puedes ver el resumen de todos tus movimientos en el dashboard: {dashboard_url}"

IMPORTANTE: Cuando uses la herramienta 'registrar_gasto', NO escribas NADA en la respuesta. Tu única acción debe ser llamar a la herramienta. Si NO vas a usar la herramienta, SÍ debes escribir una respuesta de texto."""
    
    # Definición de la herramienta para Gemini
    TOOL_DEFINITION = {
        "function_declarations": [
            {
                "name": "registrar_gasto",
                "description": "Registra un gasto o ingreso agrícola. Úsala SOLO cuando el usuario mencione un monto específico para gastar o ingresar.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "monto": {
                            "type": "number",
                            "description": "El monto numérico del gasto o ingreso. Ejemplo: 1000"
                        },
                        "categoria": {
                            "type": "string",
                            "description": "La categoría principal del gasto o ingreso.",
                            "enum": [
                                "Semillas 🌱",
                                "Fertilizantes 🧪",
                                "Agroquímicos 💧",
                                "Servicios 🛠️",
                                "Mano de Obra 🧑‍🌾",
                                "Maquinaria 🚜",
                                "Transporte 🚚",
                                "Empaque 📦",
                                "Rentas 🏠",
                                "Infraestructura 🏗️",
                                "Ingresos 💰"
                            ]
                        },
                        "descripcion": {
                            "type": "string",
                            "description": "Una descripción breve. Ejemplo: 'semilla de jitomate', 'venta de cosecha'"
                        }
                    },
                    "required": ["monto", "categoria"]
                }
            }
        ]
    }
    
    def __init__(self):
        self.settings = get_settings()
        genai.configure(api_key=self.settings.gemini_api_key)
        
        # Configurar el modelo con la herramienta
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[self.TOOL_DEFINITION]
        )
    
    async def process_message(self, user_message: str) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario con Gemini
        
        Args:
            user_message: Mensaje del usuario
            
        Returns:
            Dict con 'type' ('tool_call' o 'text') y 'data' (los datos correspondientes)
        """
        try:
            # Reemplazar {dashboard_url} en el system prompt
            system_prompt = self.SYSTEM_PROMPT.format(
                dashboard_url=self.settings.dashboard_url
            )
            
            # Crear el prompt completo
            full_prompt = f"{system_prompt}\n\nUsuario: {user_message}"
            
            # Generar respuesta
            response = self.model.generate_content(full_prompt)
            
            # Verificar si hay un tool call
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    # Si hay una función llamada
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call = part.function_call
                        
                        if function_call.name == "registrar_gasto":
                            # Extraer los argumentos
                            args = dict(function_call.args)
                            
                            # Validar con Pydantic
                            gasto = GastoTool(
                                monto=args.get("monto"),
                                categoria=args.get("categoria"),
                                descripcion=args.get("descripcion")
                            )
                            
                            return {
                                "type": "tool_call",
                                "data": gasto.model_dump()
                            }
                    
                    # Si hay texto
                    elif hasattr(part, 'text') and part.text:
                        return {
                            "type": "text",
                            "data": part.text
                        }
            
            # Si no hay respuesta válida, devolver mensaje por defecto
            return {
                "type": "text",
                "data": "Lo siento, no pude procesar tu mensaje. ¿Podrías reformularlo?"
            }
        
        except Exception as e:
            print(f"Error en Gemini: {e}")
            return {
                "type": "text",
                "data": "Disculpa, tuve un problema al procesar tu mensaje. Intenta de nuevo."
            }


# Instancia global del servicio
gemini_service = GeminiService()
