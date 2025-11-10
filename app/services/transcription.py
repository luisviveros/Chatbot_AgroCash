import io
import tempfile
from typing import Optional
from app.config import get_settings


class TranscriptionService:
    """Servicio para transcribir audio a texto"""
    
    def __init__(self):
        self.settings = get_settings()
        self.provider = self.settings.stt_provider
        
    async def transcribe_audio(self, audio_content: bytes, file_type: str) -> str:
        """
        Transcribe audio a texto usando el proveedor configurado
        
        Args:
            audio_content: Contenido del archivo de audio en bytes
            file_type: Tipo de archivo (ej: 'audio/ogg', 'audio/mp3')
            
        Returns:
            Texto transcrito
        """
        if self.provider == "google":
            return await self._transcribe_google(audio_content, file_type)
        elif self.provider == "openai":
            return await self._transcribe_openai(audio_content, file_type)
        else:
            raise ValueError(f"Proveedor STT no soportado: {self.provider}")
    
    async def _transcribe_google(self, audio_content: bytes, file_type: str) -> str:
        """Transcribe usando Google Speech-to-Text"""
        from google.cloud import speech
        
        client = speech.SpeechClient()
        
        # Detectar el encoding según el tipo de archivo
        encoding_map = {
            "audio/ogg": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            "audio/mpeg": speech.RecognitionConfig.AudioEncoding.MP3,
            "audio/mp3": speech.RecognitionConfig.AudioEncoding.MP3,
            "audio/wav": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        }
        
        encoding = encoding_map.get(
            file_type.lower(),
            speech.RecognitionConfig.AudioEncoding.OGG_OPUS
        )
        
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code="es-MX",  # Español de México
            enable_automatic_punctuation=True,
            model="default"
        )
        
        try:
            response = client.recognize(config=config, audio=audio)
            
            # Combinar todos los resultados
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            return transcript.strip() if transcript else "No se pudo transcribir el audio"
            
        except Exception as e:
            print(f"Error en Google Speech-to-Text: {e}")
            raise
    
    async def _transcribe_openai(self, audio_content: bytes, file_type: str) -> str:
        """Transcribe usando OpenAI Whisper"""
        import httpx
        
        # Determinar la extensión del archivo
        extension_map = {
            "audio/ogg": ".ogg",
            "audio/mpeg": ".mp3",
            "audio/mp3": ".mp3",
            "audio/wav": ".wav",
        }
        extension = extension_map.get(file_type.lower(), ".ogg")
        
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
            temp_file.write(audio_content)
            temp_file_path = temp_file.name
        
        try:
            # Llamar a la API de OpenAI
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(temp_file_path, "rb") as audio_file:
                    response = await client.post(
                        "https://api.openai.com/v1/audio/transcriptions",
                        headers={
                            "Authorization": f"Bearer {self.settings.openai_api_key}"
                        },
                        files={
                            "file": (f"audio{extension}", audio_file, file_type)
                        },
                        data={
                            "model": "whisper-1",
                            "language": "es"
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result.get("text", "No se pudo transcribir el audio")
        
        except Exception as e:
            print(f"Error en OpenAI Whisper: {e}")
            raise
        
        finally:
            # Limpiar el archivo temporal
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass


# Instancia global del servicio
transcription_service = TranscriptionService()
