import os
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self):
        # Configure Google Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        if api_key != "mock_key":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")

        # Use a default embedding function
        if api_key != "mock_key":
            self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=api_key
            )
        else:
            # Fallback for mock mode
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents, ids, metadatas=None):
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def query(self, user_query, n_results=3):
        # Retrieve relevant documents
        results = self.collection.query(
            query_texts=[user_query],
            n_results=n_results
        )

        context = "\n".join(results['documents'][0])

        # Construct prompt for Gemini
        prompt = f"""
        You are a helpful AI assistant. Use the following context to answer the user's query.
        If the answer is not in the context, say you don't know based on the provided information, but try to summarize what is available.

        Context:
        {context}

        Query: {user_query}

        Answer:
        """

        if os.getenv("GOOGLE_API_KEY") == "mock_key":
            return {
                "answer": f"MOCK RESPONSE: Based on the context provided, here is information about '{user_query}'. Context summary: {context[:100]}...",
                "sources": results['documents'][0],
                "metadatas": results['metadatas'][0]
            }

        response = self.model.generate_content(prompt)
        return {
            "answer": response.text,
            "sources": results['documents'][0],
            "metadatas": results['metadatas'][0]
        }

if __name__ == "__main__":
    # Quick test if run directly
    try:
        agent = RAGAgent()
        print("RAG Agent initialized successfully")
    except Exception as e:
        print(f"Error: {e}")
