# Candidate Ranking Pipeline

An optimized, two-stage evaluation pipeline designed to ingest, score, and rank candidate profiles against a target Job Description. This solution combines low-overhead dense semantic vector retrieval with a rule-based heuristic grading engine, built-in fraud detection (honeypots), and a structural validation test suite.

---

## ⚡ Quick Start (Single-Command Reproduction)

To completely reproduce the final submission `solo_sprint.csv` file directly from the raw candidate data, execute the following single command at the repository root:

```
python hybrid_ranker.py --candidates ./candidates.jsonl --out ./solo_sprint.csv 
```

---
## setup & Installation
Follow these steps to configure your local environment and prepare the required execution artifacts:

1. Clone the Repository
```
git clone <your-repository-url>
cd <your-repository-folder>
```
2. Install Pinned Dependencies
Ensure you have Python 3.10+ installed, then run:

```
pip install -r requirements.txt
```
3. Initialize Pre-computed Artifacts
Generate the localized text schemas and the FAISS vector index matrices from the candidate dataset by running the initialization scripts:

```
python preprocess.py
python build_faiss.py
```
(Note: Pre-computed index files are also tracked inside the artifacts/ folder for immediate standalone execution without retraining).

## Core Pipeline Architecture
The solution executes sequentially through distinct layers to ensure absolute modularity, data integrity, and strict runtime compliance:

Ingestion & Feature Mining (preprocess.py): Parses raw profiles using Pandas dataframes, extracts explicit skills, and pre-calculates honeypot attributes to flag structural contradictions.

Dense Vector Mapping (build_faiss.py): Converts unstructured profile details into dense matrix text embeddings and loads them into a fast, inner-product FAISS index (IndexFlatIP).

Multi-Variable Re-Ranking (hybrid_ranker.py): Pulls the retrieved pool and applies a strict mathematical weighted equation (50/15/15/10/10). It drops fraudulent records via the sanity filter, applies hard tech stack penalties, and breaks deadlocks transparently via candidate_id.

Validation Suite (check_results.py): Runs an isolated check on the generated dataset prior to output to guarantee monotonic score degradation, type safety, and exact schema alignment.

---
## Repository Structure

```text
├── artifacts/                  # Tracks pre-computed vector matrices and state embeddings
│   ├── faiss_index.bin         # Serialized high-velocity FAISS index
│   └── text_embeddings.pkl     # Pre-calculated text feature embeddings
├── preprocess.py               # Ingestion engine, schema mining, and text tokenization
├── build_faiss.py              # Compiles dense embeddings into the FAISS retrieval matrix
├── hybrid_ranker.py            # Primary execution script (Retrieval -> Re-ranking -> Export)
├── check_results.py            # Independent data integrity and validation test suite
├── requirements.txt            # Explicit third-party library manifest
├── submission_metadata.yaml    # Production metadata mirroring portal properties
└── README.md                   # Setup, execution, and architectural documentation