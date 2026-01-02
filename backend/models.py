from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

class DocumentChunk(BaseModel):
    id: str
    text: str
    metadata: dict
