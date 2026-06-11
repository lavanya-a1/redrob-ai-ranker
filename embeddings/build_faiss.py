import faiss
import numpy as np

# Load embeddings
embeddings = np.load("data/candidate_embeddings.npy")

print("Embeddings Shape:", embeddings.shape)

# Convert to float32
embeddings = embeddings.astype("float32")

# Dimension
dimension = embeddings.shape[1]

# Create Index
index = faiss.IndexFlatIP(dimension)

# Normalize vectors for cosine similarity
faiss.normalize_L2(embeddings)

# Add embeddings
index.add(embeddings)

print("Total vectors:", index.ntotal)

# Save index
faiss.write_index(index, "data/candidate_index.faiss")

print("FAISS Index Saved!")