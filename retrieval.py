from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from data_loader import load_assessments

class RetrievalSystem:
    def __init__(self, csv_path="shl_assessments.csv"):
        self.df = load_assessments(csv_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(self.df['EmbeddingText'].tolist(), show_progress_bar=True)
        self.embeddings = np.array(self.embeddings).astype('float32')
        self.dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings)

    def retrieve(self, query, k=10):
        """
        top k assessments matching the query.
        """
        query_embedding = self.model.encode([query], show_progress_bar=False)
        distances, indices = self.index.search(query_embedding, k)
        return self.df.iloc[indices[0]]

if __name__ == "__main__":
    retriever = RetrievalSystem()
    query = "Java developers who can collaborate effectively, 40 mins max"
    results = retriever.retrieve(query)
    print(results[['Name', 'Duration', 'Type']])