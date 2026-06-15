from sentence_transformers import SentenceTransformer
from docx import Document
import pandas as pd
import faiss
import numpy as np


# -----------------------------
# Load Job Description
# -----------------------------

doc = Document("data/job_description.docx")

jd_text = jd_text = """
Senior AI Engineer
Python
Embeddings
Retrieval Systems
Ranking Systems
Vector Database
Hybrid Search
Recommendation Systems
Production ML
Fine Tuning
LLM
Evaluation Metrics
FAISS
Milvus
Qdrant
OpenSearch
"""

print("Job Description Loaded")


# -----------------------------
# Load Embedding Model
# -----------------------------

print("Loading MiniLM...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Generate JD Embedding
# -----------------------------

jd_embedding = model.encode(
    [jd_text],
    convert_to_numpy=True
)

jd_embedding = jd_embedding.astype(np.float32)


# -----------------------------
# Load FAISS Index
# -----------------------------

index = faiss.read_index(
    "data/candidate_index.faiss"
)

print("FAISS Loaded")


# -----------------------------
# Retrieve Top K
# -----------------------------

TOP_K = 3000

scores, indices = index.search(
    jd_embedding,
    TOP_K
)


# -----------------------------
# Load Candidate Data
# -----------------------------

df = pd.read_parquet(
    "data/processed_candidates.parquet"
)


top_df = df.iloc[
    indices[0]
].copy()

top_df["semantic_score"] = scores[0]


# -----------------------------
# Save
# -----------------------------

top_df.to_parquet(
    "output/top1000_candidates.parquet",
    index=False
)

print(top_df.head())

print("\nSaved Top 1000 Candidates")