import os
import subprocess
import sys
import argparse

def run_script(script_path, extra_args=None):
    """Utility function to execute a Python script with optional arguments and track status."""
    print(f"\n==================================================")
    print(f"🚀 RUNNING: {script_path}")
    print(f"==================================================")
    
    # Construct the base system execution command
    cmd = [sys.executable, script_path]
    if extra_args:
        cmd.extend(extra_args)
        
    # Run the script using the current python executable environment
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode != 0:
        print(f"❌ ERROR: {script_path} failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ SUCCESS: {script_path} completed successfully.")

def main():
    # 1. Parse mandatory Hackathon CLI arguments
    parser = argparse.ArgumentParser(description="Redrob AI Ranker End-to-End Orchestrator")
    parser.add_argument('--candidates', type=str, default=os.path.join("data", "candidates.jsonl"), 
                        help="Path to the raw candidates input file")
    parser.add_argument('--out', type=str, default=os.path.join("output", "submission.csv"), 
                        help="Path where final ranked submission CSV should be saved")
    args = parser.parse_args()

    print("==================================================")
    print("   STARTING REDROB AI RANKER END-TO-END PIPELINE  ")
    print("==================================================")

    # Step 1: Preprocess the raw JSONL data into Parquet format
    # Passing the custom input candidate path down into the preprocessor step
    run_script(os.path.join("preprocess", "preprocess.py"), extra_args=["--candidates", args.candidates])

    # Step 2: Generate SentenceTransformer MiniLM Embeddings (Skipped by default for speed)
    # run_script(os.path.join("embeddings", "generate_embeddings.py"))

    # Step 3: Build the FAISS Index
    run_script(os.path.join("indexing", "build_faiss.py"))

    # Step 4: Extract Top 1000 candidates via Semantic Vector Search
    run_script(os.path.join("ranker", "retrieve_topk.py"))

    # Step 5: Execute Recruit-Style Hybrid Scoring & Disqualifiers Engine
    run_script(os.path.join("ranker", "hybrid_ranker.py"))

    # Step 6: Generate the final formatted submission file
    # Passing the custom evaluation output path directly down into the generator step
    run_script(os.path.join("ranker", "generate_submission.py"), extra_args=["--out", args.out])

    # Step 7: Final Data Integrity and Format Validator Check
    run_script(os.path.join("ranker", "validate_submission.py"), extra_args=["--out", args.out])

    print("\n==================================================")
    print(f" 🎉 PIPELINE EXECUTION COMPLETE: {args.out} READY!")
    print("==================================================")

if __name__ == "__main__":
    main()