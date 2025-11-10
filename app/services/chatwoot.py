import httpx
from typing import Optional
from app.config import get_settings


class ChatwootClient:
    """Cliente para interactuar con la API de Chatwoot"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.chatwoot_base_url
        self.api_key = self.settings.chatwoot_api_key
        
    def _get_headers(self) -> dict:
        """Headers para las peticiones a Chatwoot"""
        return {
            "api_access_token": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def send_message(
        self,
        account_id: int,
        conversation_id: int,
        content: str,
        message_type: str = "outgoing"
    ) -> dict:
        """
        Envía un mensaje a una conversación de Chatwoot
        
        Args:
            account_id: ID de la cuenta de Chatwoot
            conversation_id: ID de la conversación
            content: Contenido del mensaje
            message_type: Tipo de mensaje (outgoing por defecto)
            
        Returns:
            Respuesta de la API de Chatwoot
        """
        url = (
            f"{self.base_url}/api/v1/accounts/{account_id}"
            f"/conversations/{conversation_id}/messages"
        )
        
        payload = {
            "content": content,
            "message_type": message_type,
            "private": False
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error enviando mensaje a Chatwoot: {e}")
                raise
    
    async def download_attachment(self, data_url: str) -> bytes:
        """
        Descarga un archivo adjunto desde Chatwoot
        
        Args:
            data_url: URL del archivo en Chatwoot
            
        Returns:
            Contenido del archivo en bytes
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.get(data_url)
                response.raise_for_status()
                return response.content
            except httpx.HTTPError as e:
                print(f"Error descargando archivo: {e}")
                raise


# Instancia global del cliente
chatwoot_client = ChatwootClient()
