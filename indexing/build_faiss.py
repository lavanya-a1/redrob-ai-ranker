import numpy as np
import faiss

print("Loading embeddings...")

embeddings = np.load(
    "data/candidate_embeddings.npy"
)

embeddings = embeddings.astype(np.float32)

print("Shape:", embeddings.shape)

dimension = embeddings.shape[1]

# Cosine similarity (embeddings already normalized)
index = faiss.IndexFlatIP(dimension)

print("Building FAISS index...")

index.add(embeddings)

faiss.write_index(
    index,
    "data/candidate_index.faiss"
)

print("FAISS index saved successfully!")

print("Total vectors:", index.ntotal)