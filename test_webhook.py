#!/usr/bin/env python3
"""
Script de prueba para el backend de AgroAsistente
Ejecutar: python test_webhook.py
"""

import asyncio
import httpx
import json


async def test_text_message():
    """Prueba con un mensaje de texto"""
    payload = {
        "event": "message_created",
        "account": {"id": 1},
        "conversation": {"id": 123},
        "message_type": "incoming",
        "content": "gasté 1500 en fertilizantes para el maíz",
        "sender": {
            "id": 1,
            "phone_number": "+521234567890"
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/webhook",
            json=payload
        )
        print("📝 Test: Mensaje de texto")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("-" * 60)


async def test_greeting():
    """Prueba con un saludo"""
    payload = {
        "event": "message_created",
        "account": {"id": 1},
        "conversation": {"id": 123},
        "message_type": "incoming",
        "content": "Hola, ¿cómo estás?",
        "sender": {
            "id": 1,
            "phone_number": "+521234567890"
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/webhook",
            json=payload
        )
        print("👋 Test: Saludo")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("-" * 60)


async def test_dashboard_request():
    """Prueba solicitud de dashboard"""
    payload = {
        "event": "message_created",
        "account": {"id": 1},
        "conversation": {"id": 123},
        "message_type": "incoming",
        "content": "quiero ver el reporte",
        "sender": {
            "id": 1,
            "phone_number": "+521234567890"
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/webhook",
            json=payload
        )
        print("📊 Test: Solicitud de dashboard")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("-" * 60)


async def test_income():
    """Prueba con un ingreso"""
    payload = {
        "event": "message_created",
        "account": {"id": 1},
        "conversation": {"id": 123},
        "message_type": "incoming",
        "content": "vendí la cosecha por 25000 pesos",
        "sender": {
            "id": 1,
            "phone_number": "+521234567890"
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/webhook",
            json=payload
        )
        print("💰 Test: Ingreso")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print("-" * 60)


async def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "=" * 60)
    print("🧪 PRUEBAS DEL WEBHOOK DE AGROASISTENTE")
    print("=" * 60 + "\n")
    
    try:
        # Verificar que el servidor esté corriendo
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code != 200:
                print("❌ El servidor no está corriendo en http://localhost:8000")
                return
        
        print("✅ Servidor detectado\n")
        
        # Ejecutar pruebas
        await test_greeting()
        await asyncio.sleep(1)
        
        await test_text_message()
        await asyncio.sleep(1)
        
        await test_income()
        await asyncio.sleep(1)
        
        await test_dashboard_request()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60 + "\n")
        
    except httpx.ConnectError:
        print("❌ No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python app/main.py")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
