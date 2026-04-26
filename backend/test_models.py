#!/usr/bin/env python3
"""Test different Groq models to find working ones"""

import asyncio
import httpx
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.config import get_settings

async def test_model(model_name):
    """Test a specific model"""
    settings = get_settings()
    api_key = settings.groq_api_key
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "Hello, say 'test successful'"}
        ],
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            print(f"Model {model_name}: Status {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                if "choices" in result:
                    text = result["choices"][0]["message"]["content"]
                    print(f"  ✅ Response: {text}")
                    return True
            else:
                error_text = response.text[:100]
                print(f"  ❌ Error: {error_text}")
                return False
                
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False

async def test_all_models():
    """Test multiple models"""
    models_to_test = [
        "llama3-8b-8192",  # Original
        "llama-3.1-8b-instant",  # Working alternative
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]
    
    print("Testing Groq models...")
    working_models = []
    
    for model in models_to_test:
        if await test_model(model):
            working_models.append(model)
    
    print(f"\n✅ Working models: {working_models}")
    return working_models

if __name__ == "__main__":
    asyncio.run(test_all_models())
