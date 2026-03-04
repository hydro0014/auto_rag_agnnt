from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.rag_agent import RAGAgent
from fastapi.middleware.cors import CORSMiddleware
import os
import glob

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

def get_agent():
    global agent
    if agent is None:
        try:
            agent = RAGAgent()
            # Index sample data on startup if collection is empty
            if agent.collection.count() == 0:
                index_sample_data(agent)
        except Exception as e:
            print(f"Failed to initialize RAG Agent: {e}")
            raise e
    return agent

def index_sample_data(agent):
    data_path = "data/*.txt"
    files = glob.glob(data_path)
    if not files:
        print("No sample data found to index.")
        return

    documents = []
    ids = []
    for i, file_path in enumerate(files):
        with open(file_path, 'r') as f:
            documents.append(f.read())
            ids.append(f"doc_{i}")

    agent.add_documents(documents, ids)
    print(f"Indexed {len(documents)} documents.")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        rag_agent = get_agent()
        result = rag_agent.query(request.query)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
