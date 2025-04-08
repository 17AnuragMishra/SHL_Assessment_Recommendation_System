import logging
from retrieval import RetrievalSystem
from generation import GenerationSystem

logging.basicConfig(filename="rag_system.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class RAGSystem:
    def __init__(self, csv_path="shl_assessments.csv", gemini_api_key="AIzaSyCX_pJFcPkH2-jyaHxdju7mK6dp_v3xC7k"):
        self.retriever = RetrievalSystem(csv_path)
        self.generator = GenerationSystem(gemini_api_key)

    def recommend_assessments(self, query):
        """
        Recommend 1-10 SHL assessments based on query.
        Returns DataFrame with Name, URL, Remote, Adaptive, DurationInt, Type.
        """
        logging.info(f"Processing query: {query}")
        retrieved = self.retriever.retrieve(query, k=10)
        logging.info(f"Retrieved {len(retrieved)} assessments")
        recommendations = self.generator.generate(query, retrieved)
        logging.info(f"Generated {len(recommendations)} recommendations with columns: {recommendations.columns.tolist()}")
        return recommendations

if __name__ == "__main__":
    GEMINI_API_KEY = "AIzaSyCX_pJFcPkH2-jyaHxdju7mK6dp_v3xC7k"
    rag = RAGSystem(gemini_api_key=GEMINI_API_KEY)
    query = "Java developers who can collaborate effectively, 40 mins max"
    results = rag.recommend_assessments(query)
    print(results)