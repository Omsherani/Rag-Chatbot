
import requests
import json

try:
    print("Testing Backend at http://localhost:8000/ask...")
    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": "Hello, are you there?"},
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error connecting to backend: {e}")
