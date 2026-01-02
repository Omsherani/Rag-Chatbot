import requests
import json
import time

BASE_URL = "http://localhost:8000"

def run_verification():
    print("--- Starting Live RAG Verification ---")

    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"Health Check: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return

    # 2. Ingest Data
    ingest_text = "My name is Antigravity."
    print(f"\n[Step 1] Ingesting text: '{ingest_text}'")
    try:
        resp = requests.post(f"{BASE_URL}/ingest/text", params={"text": ingest_text})
        print(f"Ingest Response: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Ingest Failed: {e}")

    # Wait a moment for vector DB consistency (if needed)
    time.sleep(2)

    # 3. Ask Question
    question = "What is my name?"
    print(f"\n[Step 2] Asking question: '{question}'")
    try:
        resp = requests.post(f"{BASE_URL}/ask", json={"question": question})
        if resp.status_code == 200:
            print(f"Answer: {resp.json()['answer']}")
        else:
            print(f"Ask Failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Ask Request Failed: {e}")

if __name__ == "__main__":
    run_verification()
