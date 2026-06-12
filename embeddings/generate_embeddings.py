from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

print("Loading candidates...")

df = pd.read_parquet(
    "data/processed_candidates.parquet"
)

texts = df["candidate_text"].fillna("").tolist()

print("Loading MiniLM...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(

    texts,

    batch_size=64,

    show_progress_bar=True,

    convert_to_numpy=True

)

np.save(
    "data/candidate_embeddings.npy",
    embeddings
)

print(embeddings.shape)