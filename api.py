from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_system import RAGSystem
import requests
from bs4 import BeautifulSoup

GEMINI_API_KEY = "AIzaSyCX_pJFcPkH2-jyaHxdju7mK6dp_v3xC7k"
rag = RAGSystem(gemini_api_key=GEMINI_API_KEY)
class QueryInput(BaseModel):
    query: str
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Recommend SHL assessments based on job queries or JD URLs.",
    version="1.0.0"
)
@app.get("/")
async def root():
    return {"message": "Welcome to the SHL Assessment Recommendation API"}

@app.get("/recommend")
async def get_recommendations(query: str):
    """
    Get 1-10 SHL assessment recommendations for a query or JD URL.
    Returns JSON with Name, URL, Remote, Adaptive, Duration, Type.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    if query.startswith("http://") or query.startswith("https://"):
        try:
            response = requests.get(query, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            query_text = soup.get_text(separator=" ").strip()
            query_text = " ".join(query_text.split()[:200])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
    else:
        query_text = query
    recommendations = rag.recommend_assessments(query_text)
    result = recommendations.to_dict(orient="records")
    return {"recommendations": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)