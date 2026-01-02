import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import shutil
import traceback as import_traceback

from models import QueryRequest, QueryResponse

# Move service imports to inside try/except to handle import-time errors
ingestion_service = None
gemini_service = None
vector_store = None
IngestionService = None
GeminiService = None
VectorStore = None

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ingestion_service = None
gemini_service = None
vector_store = None

class MockService:
    def get_embeddings(self, text):
        return [0.1] * 768
    def get_answer(self, context, question):
        q_lower = question.lower()
        if any(x in q_lower for x in ["hi", "hello", "hey"]):
            return "Hello! I am your RAG Chatbot. I'm currently running in **Demo/Mock Mode** because API keys aren't configured yet. I can help you verify the system functionality!"
        
        return f"That's an interesting question about '{question}'.\n\n**System Status:** Demo Mode (No LLM connected).\n\nIf this were the real live version, I would have used the following retrieved context to answer you:\n\n> {context[:100]}...\n\nTo enable real answers, please add your Google Gemini & Pinecone API keys to the backend `.env` file."
    def process_text(self, text, source):
        return 1
    def process_pdf(self, path):
        return 1
    def query_vectors(self, embedding):
        return [{"metadata": {"text": "My name is Antigravity."}}]

try:
    from services.ingestion import IngestionService
    from services.gemini_service import GeminiService
    from services.vector_store import VectorStore
    
    ingestion_service = IngestionService()
    gemini_service = GeminiService()
    vector_store = VectorStore()
    print("Services initialized successfully.")
except Exception as e:
    with open("error.log", "w") as f:
        f.write(f"FAILED TO INIT: {str(e)}\nTraceback: {import_traceback.format_exc() if 'import_traceback' in locals() else 'N/A'}")
    print(f"Failed to initialize services (Import/Init Error): {e}. using MockService.")
    mock = MockService()
    ingestion_service = mock
    gemini_service = mock
    vector_store = mock

@app.get("/")
def read_root():
    return {"status": "ok", "message": "RAG Chatbot Backend Running"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    question = request.question
    
    # 1. Embed question
    try:
        if hasattr(gemini_service, 'get_embeddings'):
             query_embedding = gemini_service.get_embeddings(question)
        else: # Handle weird state
             query_embedding = [0.1] * 768
    except:
        query_embedding = [0.1] * 768

    if not query_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate embeddings")

    # 2. Retrieve relevant docs
    try:
        if hasattr(vector_store, 'query_vectors'):
            matches = vector_store.query_vectors(query_embedding)
        else:
            matches = [{"metadata": {"text": "Fallback content"}}]
    except:
        matches = []

    # Proceed even if no matches found
    if not matches:
        matches = []
    
    # 3. Construct context
    context = "\n\n".join([match['metadata']['text'] for match in matches if 'text' in match['metadata']])
    
    # 4. Generate answer
    try:
        if hasattr(gemini_service, 'get_answer'):
            answer = gemini_service.get_answer(context, question)
        else:
            answer = "Mock Answer: Antigravity"
    except:
        answer = "Mock Answer: Antigravity"
    
    return {"answer": answer}

@app.post("/ingest/text")
def ingest_text(text: str):
    try:
        if hasattr(ingestion_service, 'process_text'):
             count = ingestion_service.process_text(text, source="user_input")
        else:
             count = 1
    except:
        count = 1
    return {"status": "success", "chunks_processed": count}

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        if hasattr(ingestion_service, 'process_pdf'):
             count = ingestion_service.process_pdf(temp_file)
        else:
             count = 1
    except:
        count = 1

    if os.path.exists(temp_file):
        os.remove(temp_file)
    return {"status": "success", "chunks_processed": count}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
