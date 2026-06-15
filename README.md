# Redrob AI Ranker: Advanced Multi-Stage Talent Matching System

An enterprise-grade, recruiter-style AI candidate ranking pipeline designed for modern talent acquisition. Moving completely away from simplistic, easily manipulated keyword-matching algorithms, this system evaluates candidate suitability using **Dense Vector Semantics** combined with a robust **Deterministic Recruiter Reasoning & Behavioral Scoring Engine**.

---

## Architectural Overview

The system processes a database of **100,000+ candidates** against a specialized target Job Description using a highly optimized, two-stage retrieval and ranking pipeline:

              ┌──────────────────────────────────────┐
              │      Raw Candidates (JSONL)          │
              └──────────────────┬───────────────────┘
                                 │
                    [ Stage 1: Fast Retrieval ]
                                 ▼
              ┌──────────────────────────────────────┐
              │    Dense Vector Space (MiniLM)       │
              │   & Lightning-Fast FAISS Index       │
              └──────────────────┬───────────────────┘
                                 │ (Top 1000 Pool)
                                 ▼
                [ Stage 2: Recruiter Reasoning ]
                                 ▼
              ┌──────────────────────────────────────┐
              │     Hybrid Scoring Engine            │
              │   - Must-Have Skills Match (15%)     │
              │   - Target Experience (10%)          │
              │   - Product vs Service Match (10%)   │
              │   - Live Behavioral Signals (15%)    │
              └──────────────────┬───────────────────┘
                                 │
                    [ Hard Quality Penalty Flags ]
                                 ▼
              ┌──────────────────────────────────────┐
              │  Disqualifier Reduction Filters      │
              │  - Core Search/Retrieval Experience  │
              │  - Vector Database Familiarity       │
              └──────────────────┬───────────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────────┐
              │      Final Top 100 Output (CSV)      │
              └──────────────────────────────────────┘

---

## Scoring Methodology & Weighting Breakdown

The final rank is calculated using an advanced deterministic scoring formula. Candidates are first isolated into a Top 1000 semantic pool, then evaluated dynamically across five core categories:

* **Semantic Similarity (50% Weight):** Contextual understanding using `all-MiniLM-L6-v2` dense embeddings to analyze the core intent of profiles rather than exact phrase matches.
* **Must-Have Skills (15% Weight):** Strict validation of requested core skills (`Python`, `Embeddings`, `Retrieval`, `Ranking`, `Vector Database`).
* **Live Behavioral Signals (15% Weight):** Extracted directly from real platform interaction metrics mapped out across the dataset schema:
    * *Open to Work flag* (Max 0.30)
    * *Recruiter Response Rate* (Max 0.30)
    * *GitHub Activity Score* (Max 0.20)
    * *Notice Period Efficiency* (<= 30 days gets full 0.20; <= 60 days gets 0.10).
* **Target Experience (10% Weight):** Sweeps profile history using regular expressions. Formatted to favor the exact target tier (5–9 years gets maximum points; 4 or 10 years gets minor attenuation).
* **Product-Company Affinity (10% Weight):** Distinguishes between production-scaling backgrounds (`SaaS`, `B2B/B2C`, `Core Product`) and strictly service-oriented or client-location maintenance roles.

### Strategic Disqualifier Penalties
To combat profile inflation and keyword stuffing, hard penalties are dynamically deducted from a candidate's final score if structural essentials are missing:
* **No Core Retrieval/Search Experience:** -0.15 deduction.
* **No Vector Database Experience:** -0.10 deduction.

---

## 📁 Repository Structure

```text
redrob_ai_ranker/
├── data/
│   ├── candidates.jsonl               # Raw candidate profiles dataset
│   ├── processed_candidates.parquet   # Schema-optimized tabular dataset
│   ├── candidate_embeddings.npy       # Pre-computed dense vectors
│   ├── candidate_index.faiss          # Serialized FAISS Index database
│   └── job_description.docx           # Source evaluation requirements file
├── preprocess/
│   ├── flatten_dataset.py             # Normalizes nested JSONL attributes
│   ├── feature_builder.py             # Extracts/calculates base pipeline variables
│   └── preprocess.py                  # Initial parsing and ingestion pipeline
├── embeddings/
│   └── generate_embeddings.py         # MiniLM text embedding script
├── indexing/
│   └── build_faiss.py                 # Index assembly and vector normalization
├── ranker/
│   ├── jd_parser.py                   # Contextual extraction of job document text
│   ├── retrieve_topk.py               # Top 1000 vector search isolation
│   ├── hybrid_ranker.py               # Heavy multi-stage scoring algorithm
│   ├── generate_submission.py         # Submissions format compiler
│   └── validate_submission.py         # Format/Integrity validation test suite
├── output/
│   ├── top1000_candidates.parquet     # Mid-stage semantic query results
│   ├── final_ranked_candidates.csv    # Full analytical matrix breakdown
│   └── submission.csv                 # Final submission file
├── main.py                            # Central pipeline orchestration script
├── .gitignore                         # Excludes large binaries and venv tracking
├── README.md                          # documentation
└── requirements.txt                   # environment dependencies