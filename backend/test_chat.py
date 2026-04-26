#!/usr/bin/env python3
"""Test script to verify chat endpoint"""

import requests
import json

def test_chat_endpoint():
    """Test the chat endpoint with a simple message"""
    url = "http://localhost:8000/api/chat/message"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": "Hello, how are you?",
        "language": "en"
    }
    
    try:
        print("Testing chat endpoint...")
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"Reply: {result.get('reply', '')[:100]}...")
            print(f"Source: {result.get('source')}")
            print(f"Model: {result.get('model')}")
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_chat_endpoint()
