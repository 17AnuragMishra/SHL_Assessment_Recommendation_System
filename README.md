Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline to recommend 1–10 SHL assessments based on user input. It features a Streamlit web app and a FastAPI endpoint, deployed on Render.

Features

*   Input: Natural language queries (e.g., "Java developers, 40 mins max") or JD URLs.
    
*   Output: Table/JSON with Name (hyperlinked), URL, Remote, Adaptive, Duration, Type.
    
*   Tech Stack: Python, SentenceTransformers, FAISS, Gemini API, Streamlit, FastAPI.
    

Repository Structure

*   data\_loader.py: Loads and prepares CSV data
    
*   retrieval.py: FAISS-based retrieval system
    
*   generation.py: Gemini API generation logic
    
*   rag\_system.py: Combines retrieval and generation
    
*   web\_app.py: Streamlit web application
    
*   api.py: FastAPI endpoint
    
*   shl\_assessments.csv: Dataset with 26 SHL assessments
    
*   requirements.txt: Dependencies
    
*   README.md: This file
    

Setup

1.  Clone the Repository:git clone [https://github.com/yourusername/shl-assessment-recommender.git](https://github.com/yourusername/shl-assessment-recommender.git)cd shl-assessment-recommender
    
2.  Install Dependencies:
    
    *   Requires Python 3.11.python -m venv .venvsource .venv/bin/activate (On Windows: .venv\\Scripts\\activate)pip install -r requirements.txt
        
3.  Add Gemini API Key:
    
    *   Replace "your-api-key-here" in rag\_system.py, generation.py, and api.py with your Gemini API key from [https://ai.google.dev/](https://ai.google.dev/).
        

UsageRun Locally

*   Web App:streamlit run web\_app.py
    
    *   Open [http://localhost:8501](http://localhost:8501), enter a query or URL, and click "Get Recommendations."
        
*   API:uvicorn api:app --reload
    
    *   Test: [http://127.0.0.1:8000/recommend?query=Java developers who can collaborate effectively, 40 mins max](http://127.0.0.1:8000/recommend?query=Java developers who can collaborate effectively, 40 mins max)
        

Deployed Services

*   Web App: [https://shl-assessment-recommendation-system-7cen.onrender.com/](https://shl-assessment-recommendation-system-7cen.onrender.com/)
    
*   API: [http://shl-assessment-recommendation-system-api.onrender.com/recommend](http://shl-assessment-recommendation-system-api.onrender.com/recommend)
    

DeploymentHosted on Render’s free tier:

*   Web App: streamlit run web\_app.py --server.port $PORT --server.address 0.0.0.0
    
*   API: uvicorn api:app --host 0.0.0.0 --port $PORT
    

Evaluation

*   Accuracy: Mean Recall@3 ≈ 0.525, MAP@3 ≈ 0.695 (manual benchmark with 26 entries).
    
*   Logs: Tracing in rag\_system.log.
    

Notes

*   Limited to 36 assessments—expandable with a larger dataset.
    
*   Built for an SHL GenAI assessment, submitted April 2025.
    

LicenseMIT License—feel free to adapt and reuse!
