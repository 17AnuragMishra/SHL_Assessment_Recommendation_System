from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_system import RAGSystem
import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
import logging

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

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint to verify API is running."""
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/recommend", response_class=JSONResponse)
async def get_recommendations(data: QueryInput):
    """
    Get 1-10 SHL assessment recommendations for a query or JD URL.
    """
    try:
        query = data.query
        if not query:
            raise HTTPException(status_code=400, detail="Query field is required")
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
        formatted_response = {
            "recommended_assessments": [
                {
                    "url": row["URL"],
                    "adaptive_support": "Yes" if row["Adaptive"] == "Yes" else "No",
                    "description": row["Name"],  # Adjust if description exists
                    "duration": row.get("DurationInt", int(row["Duration"].replace(" mins", "")) if "Duration" in row else 0),
                    "remote_support": "Yes" if row["Remote"] == "Yes" else "No",
                    "test_type": row["Type"].split(", ") if isinstance(row["Type"], str) else [row["Type"]]
                } for row in result[:10]
            ]
        }
        logging.info(f"Processed query: {query}, returned {len(formatted_response['recommended_assessments'])} assessments")
        return JSONResponse(content=formatted_response, status_code=200)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error processing recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)