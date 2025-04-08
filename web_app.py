import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from rag_system import RAGSystem

GEMINI_API_KEY = "AIzaSyCX_pJFcPkH2-jyaHxdju7mK6dp_v3xC7k"
rag = RAGSystem(gemini_api_key=GEMINI_API_KEY)

st.title("SHL Assessment Recommendation System")
st.write("Enter a job query or JD URL to get tailored SHL assessment recommendations.")
input_type = st.radio("Input Type:", ("Natural Language Query", "Job Description URL"))
user_input = st.text_input("Enter your query or URL here:")

if st.button("Get Recommendations"):
    """
    Here we have two options -
        1. JD using URL
        2. Using input text box
    """
    if user_input:
        if input_type == "Natural Language Query":
            query = user_input
        else:
            try:
                response = requests.get(user_input, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                query = soup.get_text(separator=" ").strip()
                query = " ".join(query.split()[:200])  # Limit to 200 words
            except Exception as e:
                st.error(f"Error fetching URL: {e}")
                query = None
        if query:
            with st.spinner("Generating recommendations..."):
                recommendations = rag.recommend_assessments(query)
                recommendations['Name'] = recommendations.apply(
                    lambda row: f"[{row['Name']}]({row['URL']})", axis=1
                )
                st.write(f"Top {len(recommendations)} Recommended Assessments:")
                st.table(recommendations[['Name', 'Remote', 'Adaptive', 'DurationInt', 'Type']])
    else:
        st.warning("Please enter a query or URL.")

st.write("Hope you like my efforts, Built with Streamlit and SHL Product Catalog data.")

if __name__ == "__main__":
    pass