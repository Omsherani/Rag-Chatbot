
import sys
import os

# Mimic main.py path setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Attempting imports...")
    from services.ingestion import IngestionService
    from services.gemini_service import GeminiService
    from services.vector_store import VectorStore
    print("Imports successful.")

    gemini = GeminiService()
    if gemini.model is None:
        print("GeminiService: Mock Mode (API Key issue)")
    else:
        print("GeminiService: Live Mode")

except Exception as e:
    print(f"FAILED: {e}")
