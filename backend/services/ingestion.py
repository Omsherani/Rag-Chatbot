import os
from pypdf import PdfReader
from typing import List
from .gemini_service import GeminiService
from .vector_store import VectorStore
import uuid

class IngestionService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.vector_store = VectorStore()

    def process_text(self, text: str, source: str = "text_input"):
        chunks = self._chunk_text(text)
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = self.gemini_service.get_embeddings(chunk)
            if embedding:
                vector_id = f"{source}_{i}_{str(uuid.uuid4())[:8]}"
                metadata = {"text": chunk, "source": source}
                vectors.append((vector_id, embedding, metadata))
        
        if vectors:
            self.vector_store.upsert_vectors(vectors)
            return len(vectors)
        return 0

    def process_pdf(self, file_path: str):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return self.process_text(text, source=os.path.basename(file_path))
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return 0

    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)
        return chunks
