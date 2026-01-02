
import requests
import json
import time

url = "http://localhost:8000/ask"
headers = {"Content-Type": "application/json"}

questions = ["Hi", "Who are you?"]

for q in questions:
    payload = {"question": q}
    try:
        print(f"Sending Question: {q}")
        response = requests.post(url, json=payload, headers=headers)
        print("--- RESPONSE ---")
        print(response.json().get('answer', 'No answer field'))
        print("----------------\n")
        time.sleep(1) 
    except Exception as e:
        print(f"Error: {e}")
