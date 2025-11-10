from app.models.schemas import ChatwootWebhookPayload
from app.services.chatwoot import chatwoot_client
from app.services.transcription import transcription_service
from app.services.gemini import gemini_service
from app.services.bigquery import bigquery_service


class WebhookHandler:
    """Manejador principal del webhook de Chatwoot"""
    
    @staticmethod
    async def process_webhook(payload: ChatwootWebhookPayload) -> dict:
        """
        Procesa el webhook de Chatwoot
        
        Args:
            payload: Datos del webhook
            
        Returns:
            Resultado del procesamiento
        """
        try:
            # 1. Validar que sea un mensaje entrante
            if payload.message_type != "incoming":
                return {
                    "success": True,
                    "message": "Mensaje ignorado (no es incoming)",
                    "skipped": True
                }
            
            # 2. Obtener el ID del usuario (número de WhatsApp)
            id_usuario = None
            if payload.sender and payload.sender.phone_number:
                id_usuario = payload.sender.phone_number
            else:
                id_usuario = str(payload.conversation.id)  # Fallback al conversation ID
            
            # 3. Determinar si es texto o audio
            texto_usuario = None
            
            if payload.content:
                # Es un mensaje de texto
                texto_usuario = payload.content
                print(f"📝 Mensaje de texto recibido: {texto_usuario}")
            
            elif payload.attachments and len(payload.attachments) > 0:
                # Es un mensaje de audio
                attachment = payload.attachments[0]
                
                if "audio" not in attachment.file_type.lower():
                    # No es audio, enviar mensaje de error
                    await chatwoot_client.send_message(
                        account_id=payload.account.id,
                        conversation_id=payload.conversation.id,
                        content="⚠️ Solo puedo procesar mensajes de texto y notas de voz."
                    )
                    return {
                        "success": True,
                        "message": "Archivo no soportado",
                        "skipped": True
                    }
                
                print(f"🎤 Audio recibido: {attachment.data_url}")
                
                # Descargar el audio
                audio_content = await chatwoot_client.download_attachment(
                    attachment.data_url
                )
                
                # Transcribir el audio
                texto_usuario = await transcription_service.transcribe_audio(
                    audio_content=audio_content,
                    file_type=attachment.file_type
                )
                
                print(f"✅ Audio transcrito: {texto_usuario}")
            
            else:
                # No hay contenido procesable
                return {
                    "success": True,
                    "message": "Sin contenido procesable",
                    "skipped": True
                }
            
            # 4. Procesar con Gemini
            gemini_response = await gemini_service.process_message(texto_usuario)
            
            # 5. Actuar según la respuesta de Gemini
            if gemini_response["type"] == "tool_call":
                # CASO 1: La IA quiere registrar un gasto
                await WebhookHandler._handle_tool_call(
                    payload=payload,
                    gasto_data=gemini_response["data"],
                    id_usuario=id_usuario
                )
            
            elif gemini_response["type"] == "text":
                # CASO 2: La IA responde con texto (saludo o dashboard)
                await WebhookHandler._handle_text_response(
                    payload=payload,
                    text=gemini_response["data"]
                )
            
            return {
                "success": True,
                "message": "Webhook procesado exitosamente",
                "data": gemini_response
            }
        
        except Exception as e:
            print(f"❌ Error procesando webhook: {e}")
            
            # Enviar mensaje de error al usuario
            try:
                await chatwoot_client.send_message(
                    account_id=payload.account.id,
                    conversation_id=payload.conversation.id,
                    content="❌ Disculpa, hubo un error procesando tu mensaje. Por favor, intenta de nuevo."
                )
            except:
                pass
            
            raise
    
    @staticmethod
    async def _handle_tool_call(
        payload: ChatwootWebhookPayload,
        gasto_data: dict,
        id_usuario: str
    ):
        """Maneja el caso donde la IA usa la herramienta registrar_gasto"""
        
        # Insertar en BigQuery
        record = await bigquery_service.insert_gasto(
            id_usuario=id_usuario,
            monto=gasto_data["monto"],
            categoria=gasto_data["categoria"],
            descripcion=gasto_data.get("descripcion")
        )
        
        # Preparar mensaje de confirmación
        mensaje_confirmacion = (
            f"✅ ¡Gasto registrado!\n\n"
            f"💰 Monto: ${gasto_data['monto']:,.2f}\n"
            f"📂 Categoría: {gasto_data['categoria']}\n"
        )
        
        if gasto_data.get("descripcion"):
            mensaje_confirmacion += f"📝 Descripción: {gasto_data['descripcion']}\n"
        
        mensaje_confirmacion += f"\n🔍 ID: {record['id_gasto'][:8]}..."
        
        # Enviar confirmación a Chatwoot
        await chatwoot_client.send_message(
            account_id=payload.account.id,
            conversation_id=payload.conversation.id,
            content=mensaje_confirmacion
        )
        
        print(f"✅ Gasto registrado y confirmación enviada")
    
    @staticmethod
    async def _handle_text_response(
        payload: ChatwootWebhookPayload,
        text: str
    ):
        """Maneja el caso donde la IA responde con texto"""
        
        # Enviar el texto directamente a Chatwoot
        await chatwoot_client.send_message(
            account_id=payload.account.id,
            conversation_id=payload.conversation.id,
            content=text
        )
        
        print(f"💬 Respuesta de texto enviada")


# Instancia global del handler
webhook_handler = WebhookHandler()
