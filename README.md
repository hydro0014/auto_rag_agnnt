# AI RAG Agent with Google Gemini & ChromaDB

This is a modern AI agent that uses Retrieval-Augmented Generation (RAG) to summarize information from your local documents. It features a FastAPI backend, ChromaDB for vector storage, Google Gemini for intelligent summarization, and a sleek React frontend styled with Tailwind CSS.

## Features

- **RAG Architecture**: Retrieves relevant context from local documents before generating answers.
- **Vector Database**: Uses ChromaDB to store and search document embeddings.
- **Google Gemini**: Leverages Google's state-of-the-art LLM for high-quality summarization.
- **Modern UI**: A clean, responsive "fresh vibe" interface built with React and Tailwind CSS.

## Prerequisites

- Python 3.10+
- Node.js 18+
- A Google AI API Key (Get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd auto_rag_agnnt
```

### 2. Backend Setup

1. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory or export the variable:
   ```bash
   export GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 3. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

### 1. Start the Backend Server

From the root directory:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
The backend will automatically index the sample documents in the `data/` folder on the first run.

### 2. Start the Frontend Development Server

In a new terminal, navigate to the `frontend` directory:
```bash
npm run dev
```
Open your browser to the URL provided by Vite (usually `http://localhost:5173`).

## Usage

1. Type your question into the search bar (e.g., "What is Gemini?").
2. Click "Query Agent".
3. The agent will retrieve relevant information from the `data/` folder and provide a summarized answer.
4. You can view the original sources used for the summary below the answer.

## Project Structure

- `backend/`: FastAPI application and RAG logic.
- `frontend/`: React + Vite + Tailwind CSS frontend.
- `data/`: Sample text documents for the agent to index.
- `chroma_db/`: Persistent storage for the vector database.
