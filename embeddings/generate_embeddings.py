import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading candidates...")

df = pd.read_parquet(
    "data/processed_candidates.parquet"
)

texts = df["embedding_text"].fillna("").tolist()

print("Loading MiniLM...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(

    texts,

    batch_size=64,

    show_progress_bar=True,

    convert_to_numpy=True,

    normalize_embeddings=True

)

np.save(

    "data/candidate_embeddings.npy",

    embeddings

)

print("Saved candidate_embeddings.npy")
print(embeddings.shape)