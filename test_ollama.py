#!/usr/bin/env python3
"""
Test script to verify Ollama connectivity and available models.
"""

import requests
import json
from typing import List, Dict

def test_ollama_connection(base_url: str = "http://localhost:11434") -> bool:
    """Test if Ollama is running and accessible."""
    try:
        response = requests.get(f"{base_url}/api/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"✅ Ollama is running! Version: {version_info.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Ollama responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Is it running?")
        print("   Try: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error testing Ollama connection: {e}")
        return False

def list_ollama_models(base_url: str = "http://localhost:11434") -> List[Dict]:
    """List available Ollama models."""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"\n📋 Available Ollama models ({len(models)}):")
            for model in models:
                name = model.get('name', 'unknown')
                size = model.get('size', 0)
                size_gb = size / (1024**3) if size else 0
                modified = model.get('modified_at', 'unknown')[:10]  # Just date part
                print(f"   • {name:<20} {size_gb:.1f}GB  (modified: {modified})")
            return models
        else:
            print(f"❌ Failed to list models: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return []

def test_ollama_chat(model: str = "llama3.2:latest", base_url: str = "http://localhost:11434") -> bool:
    """Test chat completion with Ollama."""
    try:
        # Use OpenAI-compatible endpoint
        url = f"{base_url}/v1/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'Hello from Ollama!' and nothing else."}
            ],
            "max_tokens": 50
        }
        
        print(f"\n🧪 Testing chat with model: {model}")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            message = data['choices'][0]['message']['content']
            print(f"✅ Chat test successful!")
            print(f"   Response: {message.strip()}")
            return True
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing chat: {e}")
        return False

def main():
    """Run Ollama connectivity tests."""
    print("🤖 LGTM Bot - Ollama Connectivity Test")
    print("=" * 40)
    
    # Test basic connection
    if not test_ollama_connection():
        print("\n💡 To fix:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Run: ollama serve")
        print("   3. Pull a model: ollama pull llama3.2:latest")
        return False
    
    # List available models
    models = list_ollama_models()
    if not models:
        print("\n💡 No models found. Try pulling one:")
        print("   ollama pull llama3.2:latest")
        return False
    
    # Test chat with the first available model
    first_model = models[0]['name']
    success = test_ollama_chat(first_model)
    
    if success:
        print(f"\n🎉 Ollama is ready for LGTM Bot!")
        print(f"\nTo use with LGTM Bot:")
        print(f"   1. Copy: cp config-ollama.yaml config.yaml")
        print(f"   2. Edit config.yaml to set model: '{first_model}'")
        print(f"   3. Run: python lgtm_bot.py PROJ-123")
    else:
        print(f"\n❌ Ollama is running but chat failed.")
        print(f"   Try a different model or check Ollama logs.")
    
    return success

if __name__ == "__main__":
    main() 