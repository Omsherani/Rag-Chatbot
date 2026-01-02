from pinecone import Pinecone
import os
from typing import List, Dict
import random

class VectorStore:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index = None
        self.mock_store = {} # In-memory store for mock mode

        if not self.api_key:
            print("Warning: PINECONE_API_KEY not found. Running in MOCK MODE (In-memory).")
            return

        try:
            pc = Pinecone(api_key=self.api_key)
            index_name = os.getenv("PINECONE_INDEX_NAME", "rag-chatbot")
            self.index = pc.Index(index_name)
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            self.index = None

    def upsert_vectors(self, vectors: List[tuple]):
        # vectors format: (id, values, metadata)
        if self.index:
            try:
                self.index.upsert(vectors=vectors)
            except Exception as e:
                print(f"Error upserting vectors: {e}")
        else:
            # Mock mode: store in memory
            for vec_id, values, metadata in vectors:
                self.mock_store[vec_id] = {"id": vec_id, "values": values, "metadata": metadata}

    def query_vectors(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        if self.index:
            try:
                results = self.index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True
                )
                return results['matches']
            except Exception as e:
                print(f"Error querying vector store: {e}")
                return []
        else:
            # Mock mode: return all docs (simple brute force or just top N)
            # Since embeddings are random, we just return the most recently added for demo
            matches = []
            for vec in self.mock_store.values():
                matches.append({
                    "id": vec["id"],
                    "score": 0.9, # Fake score
                    "metadata": vec["metadata"]
                })
            return matches[:top_k]
