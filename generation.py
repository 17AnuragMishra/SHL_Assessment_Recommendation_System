import requests
import pandas as pd

class GenerationSystem:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    def generate(self, query, retrieved_df):
        """
        Generate recommendations from retrieved assessments.
        """
        max_duration = 60  # Default
        if "mins" in query.lower():
            try:
                max_duration = int(query.lower().split("max")[1].split("mins")[0].strip())
            except:
                pass
        filtered_df = retrieved_df[retrieved_df['DurationInt'] <= max_duration].copy()

        prompt = f"""
        Given this query: '{query}'
        And these assessments:
        {filtered_df[['Name', 'URL', 'Remote', 'Adaptive', 'DurationInt', 'Type']].to_string(index=False)}
        Recommend 1-10 assessments that best match the query. Return results in a table with:
        - Assessment Name (with URL as hyperlink, e.g., [Name](URL))
        - Remote Testing Support
        - Adaptive/IRT Support
        - Duration
        - Test Type
        Sort by relevance and respect duration constraints (max {max_duration} mins).
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3}
        }
        response = requests.post(f"{self.api_url}?key={self.api_key}", json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()['candidates'][0]['content']['parts'][0]['text']
            return filtered_df.head(10)[['Name', 'URL', 'Remote', 'Adaptive', 'DurationInt', 'Type']]
        else:
            print(f"API Error: {response.text}")
            return filtered_df.head(10)[['Name', 'URL', 'Remote', 'Adaptive', 'DurationInt', 'Type']]

if __name__ == "__main__":
    GEMINI_API_KEY = "AIzaSyCX_pJFcPkH2-jyaHxdju7mK6dp_v3xC7k"
    generator = GenerationSystem(GEMINI_API_KEY)
    sample_df = pd.DataFrame({
        "Name": ["Python Coding Test", "Verify G+"],
        "URL": ["https://shl.com/python", "https://shl.com/verify"],
        "Remote": ["Yes", "Yes"],
        "Adaptive": ["No", "Yes"],
        "Duration": ["25 mins", "30 mins"],
        "Type": ["Skills", "Cognitive"],
        "DurationInt": [25, 30]
    })
    query = "Python developers, 30 mins max"
    results = generator.generate(query, sample_df)
    print(results)