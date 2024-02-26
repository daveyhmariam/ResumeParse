#!/usr/bin/python3
import pandas as pd
from pyresparser import ResumeParser
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
import string
import textract

# Function to clean text (replace with your desired cleaning steps)
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    import string
    text = "".join([char for char in text if char not in string.punctuation])
    # Remove stop words (optional)
    # from nltk.corpus import stopwords
    # stop_words = stopwords.words('english')
    # text = " ".join([word for word in text.split() if word not in stop_words])
    return text


# Load spaCy model (download English language model if needed)
nlp = spacy.load("en_core_web_sm")


# Function to extract relevant information from CV
def extract_cv_text(cv_path):

    text = textract.process(cv_path, encoding='utf-8').decode('utf-8')
    data = ResumeParser(text).get_extracted_data()

    # Extract desired information (example):
    skills = data.get("skills", [])
    experience = data.get("work_experience", [])
    education = data.get("education", [])

    # Combine extracted information (adjust based on your needs)
    extracted_text = " ".join([
        ", ".join(skills),
        " ".join([exp["company"] + ", " + exp["title"] for exp in experience]),
        " ".join([edu["institution"] + ", " + edu["degree"] for edu in education])
    ])

    return clean_text(extracted_text)


# Read CVs and extract text
cv_data = pd.DataFrame()
cvs = "/home/dave/Downloads/Dawit/Dawit/dv"
for filename in os.listdir(cvs):
    cv_path = os.path.join(cvs, filename)
    text = extract_cv_text(cv_path)
    cv_data = cv_data.append({"text": text}, ignore_index=True)

# Preprocess Job Description
with open("/home/dave/Downloads/Dawit/IOCC MNHT - Emergency H and N Project Coordinator.doc", "r", encoding=["utf-8", "ISO-8859-1", "latin-1"]) as f:
    jd_text = f.read()
jd_text = clean_text(jd_text)

# Vectorize CVs and JD
vectorizer = TfidfVectorizer()
cv_vectors = vectorizer.fit_transform(cv_data["text"])
jd_vector = vectorizer.transform([jd_text])

# Calculate cosine similarity scores
similarities = np.dot(cv_vectors, jd_vector.T).toarray()[0]

# Define a threshold for ranking (adjust based on your needs)
threshold = 0.7

# Rank and analyze CVs
ranked_cvs = pd.DataFrame({"CV": cv_data["text"], "Similarity Score": similarities})
ranked_cvs = ranked_cvs.sort_values(by="Similarity Score", ascending=False)

# Print top 10 most relevant CVs
print("Top 10 Most Relevant CVs:")
print(ranked_cvs.head(10))

# Analyze and prioritize CVs based on scores and your criteria
# (e.g., manually review "highly relevant" CVs)
print("\nFurther analysis and prioritization needed based on scores and specific needs.")
