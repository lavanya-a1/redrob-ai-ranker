from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from tqdm import tqdm
import os


# -----------------------------
# Load Processed Candidate Data
# -----------------------------

DATA_PATH = "data/processed_candidates.parquet"

print("Loading processed candidates...")

df = pd.read_parquet(DATA_PATH)

print(f"Loaded {len(df)} candidates")


# -----------------------------
# Load Embedding Model
# -----------------------------

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")


# -----------------------------
# Generate Embeddings
# -----------------------------

texts = df["combined_text"].fillna("").tolist()

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True
)


# -----------------------------
# Save Embeddings
# -----------------------------

OUTPUT_PATH = "data/candidate_embeddings.npy"

np.save(OUTPUT_PATH, embeddings)

print("\nEmbeddings saved successfully!")

print(f"Shape : {embeddings.shape}")

print(f"Saved at : {OUTPUT_PATH}")