import os
import subprocess
import sys

def run_script(script_path):
    """Utility function to execute a Python script and track its status."""
    print(f"\n==================================================")
    print(f"🚀 RUNNING: {script_path}")
    print(f"==================================================")
    
    # Run the script using the current python executable environment
    result = subprocess.run([sys.executable, script_path], capture_output=False)
    
    if result.returncode != 0:
        print(f"❌ ERROR: {script_path} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ SUCCESS: {script_path} completed successfully.")

def main():
    print("==================================================")
    print("   STARTING REDROB AI RANKER END-TO-END PIPELINE  ")
    print("==================================================")

    # Step 1: Preprocess the raw JSONL data into Parquet format
    run_script(os.path.join("preprocess", "preprocess.py"))

    # Step 2: Generate SentenceTransformer MiniLM Embeddings
    # NOTE: This step is computationally heavy. Since you already generated 
    # candidate_embeddings.npy, we can safely skip or include it.
    # Un-comment the line below if a clean database re-run is needed:
    # run_script(os.path.join("embeddings", "generate_embeddings.py"))

    # Step 3: Build the FAISS Index
    run_script(os.path.join("indexing", "build_faiss.py"))

    # Step 4: Extract Top 1000 candidates via Semantic Vector Search
    run_script(os.path.join("ranker", "retrieve_topk.py"))

    # Step 5: Execute Recruit-Style Hybrid Scoring & Disqualifiers Engine
    run_script(os.path.join("ranker", "hybrid_ranker.py"))

    # Step 6: Generate the final formatted submission file
    run_script(os.path.join("ranker", "generate_submission.py"))

    # Step 7: Final Data Integrity and Format Validator Check
    run_script(os.path.join("ranker", "validate_submission.py"))

    print("\n==================================================")
    print(" 🎉 PIPELINE EXECUTION COMPLETE: submission.csv READY!")
    print("==================================================")

if __name__ == "__main__":
    main()