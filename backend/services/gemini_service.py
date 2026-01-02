import google.generativeai as genai
import os
import random

class GeminiService:
    def __init__(self):
        try:
            self.api_key = os.getenv("GOOGLE_API_KEY")
            # Handle both None and empty string
            if not self.api_key or self.api_key.strip() == "":
                with open("gemini_debug.log", "w") as f:
                    f.write(f"API Key Missing. Env: {os.environ.keys()}")
                print("Warning: GOOGLE_API_KEY not found or empty. Running in MOCK MODE.")
                self.model = None
                self.api_key = None # Force to None for checks
            else:
                with open("gemini_debug.log", "w") as f:
                    f.write(f"API Key Found: {self.api_key[:5]}...")
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            with open("gemini_error.log", "w") as f:
                f.write(f"Gemini Init Error: {e}")
            print(f"Error initializing Gemini: {e}")
            self.model = None
            self.api_key = None
    
    def get_embeddings(self, text: str) -> list[float]:
        # ... (unchanged code) ...
        # NOTE: I need to be careful not to delete get_embeddings, so I will target the get_answer method instead for the logic check.
        # But this tool doesn't support "skipping" lines in ReplacementContent easily if I target a large block.
        # I will do two separate edits.

        if not self.api_key:
            # Return random 768-dim vector (Geneartive AI usually 768)
            return [random.random() for _ in range(768)]

        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document",
                title="Embedding of single string"
            )
            return result['embedding']
        except Exception as e:
            with open("gemini_runtime.log", "w") as f:
                f.write(f"Embedding Error: {e}")
            print(f"Error generating embeddings: {e}")
            return []

    def get_answer(self, context: str, question: str) -> str:
        # Hardcoded responses for specific persona compliance
        q_lower = question.strip().lower()
        if q_lower in ["hi", "hello", "hey", "hi!", "hello!"]:
            return "Hi, Hope you are doing well, How I can Assit you?"
        if any(x in q_lower for x in ["who are you", "what are you"]):
            return "I am a Retrieval-Augmented AI Chatbot designed to provide accurate, context-aware answers.\n\nThink of me as your intelligent knowledge assistant. I combine advanced language understanding with a curated knowledge base to deliver responses that are relevant, reliable, and grounded in real information."

        if not self.api_key:
            return f"[MOCK ANSWER] Based on the context provided:\n\n{context[:200]}...\n\nI can answer '{question}' as 'Antigravity' (Verified Mock)."

        prompt = f"""
        You are a Retrieval-Augmented AI Chatbot.

        Instructions:
        1. Use the provided Context below to answer the user's question.
        2. If the Context is empty or does not contain the answer, IGNORE the context and answer using your general knowledge.
        3. If the user says "Hi", "Hello", or similar greetings, respond EXACTLY with: "Hi, Hope you are doing well, How I can Assit you?"
        4. If the user asks "who are you" or "what are you", respond EXACTLY with: "I am a Retrieval-Augmented AI Chatbot designed to provide accurate, context-aware answers.

Think of me as your intelligent knowledge assistant. I combine advanced language understanding with a curated knowledge base to deliver responses that are relevant, reliable, and grounded in real information."

        Context:
        {context}
        
        Question:
        {question}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {e}"
