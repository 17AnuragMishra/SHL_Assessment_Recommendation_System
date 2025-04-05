import pandas as pd
def load_assessments(csv_path="shl_assessments.csv"):
    """
    We have created a CSV file so loading the data from it.
    Expected columns(as required for the assessment): Name, URL, Remote, Adaptive, Duration, Type
    """
    df = pd.read_csv(csv_path, on_bad_lines='warn')
    required_columns = ["Name", "URL", "Remote", "Adaptive", "Duration", "Type"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain: {required_columns}")
    df['EmbeddingText'] = df['Name'] + " " + df['Type']
    df['DurationInt'] = df['Duration'].str.replace(" mins", "").astype(int)
    return df
if __name__ == "__main__":
    assessments = load_assessments()
    print(assessments.head())