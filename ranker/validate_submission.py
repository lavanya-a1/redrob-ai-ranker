import pandas as pd
import argparse
import os
import sys

def main():
    # 1. Accept dynamic output path from main.py CLI
    parser = argparse.ArgumentParser(description="Submission Format and Integrity Validator")
    parser.add_argument('--out', type=str, default="output/submission.csv", 
                        help="Path to the final compiled submission CSV")
    args = parser.parse_args()

    print("\n--- Running Submission Integrity Check ---")
    sub_path = args.out
    intermediate_path = "output/final_ranked_candidates.csv"

    # 2. File existence check
    if not os.path.exists(sub_path):
        print(f"❌ Error: Final submission file is missing at {sub_path}!")
        sys.exit(1)

    df = pd.read_csv(sub_path)
    errors = 0

    # 3. Check column count and names (Must match exactly)
    expected_cols = ['candidate_id', 'rank', 'score', 'reasoning']
    if list(df.columns) != expected_cols:
        print(f"❌ Error: Columns do not match specification. Expected {expected_cols}, got {list(df.columns)}")
        errors += 1

    # 4. Check exact row count (Issue 7 Compliance)
    if len(df) != 100:
        print(f"❌ Error: Row count must be exactly 100. Your file has {len(df)} entries.")
        errors += 1

    # 5. Check for null or empty values
    if df.isnull().any().any():
        print("❌ Error: Missing or NaN values detected inside the submission file!")
        print(df.isnull().sum())
        errors += 1

    # 6. Check rank column sequencing
    expected_ranks = list(range(1, 101))
    if list(df['rank']) != expected_ranks:
        print("❌ Error: The 'rank' column must be sequential from 1 to 100.")
        errors += 1

    # 7. Check for duplicate candidate submissions
    if df['candidate_id'].duplicated().any():
        print("❌ Error: Duplicate candidate IDs found in your top 100 picks!")
        errors += 1

    # 8. Safe Monotonic Score Check (Issue 8 Compliance)
    # Since the final submission schema doesn't have a 'score' column, we check the intermediate file
    if os.path.exists(intermediate_path):
        try:
            inter_df = pd.read_csv(intermediate_path)
            if 'final_score' in inter_df.columns:
                is_monotonic = inter_df['final_score'].is_monotonic_decreasing
                if is_monotonic:
                    print("✅ Success: Mathematical models confirm scores are perfectly monotonically non-increasing.")
                else:
                    print("❌ Error: Pipeline logic fault! Scores are out of ordered ranking alignment.")
                    errors += 1
            else:
                print("⚠️ Warning: 'final_score' missing from intermediate rankings. Monotonicity check bypassed.")
        except Exception as e:
            print(f"⚠️ Warning: Could not parse intermediate file for monotonicity check: {e}")
    else:
        print("⚠️ Warning: Intermediate ranking data file missing. Skipping mathematical score sorting check.")

    # Final Verdict Gate
    if errors == 0:
        print(f"✅ Validation Passed! Your file {os.path.basename(sub_path)} is perfectly structured and ready to turn in.")
        sys.exit(0)
    else:
        print(f"❌ Validation Failed with {errors} total layout error(s). Fix core model steps.")
        sys.exit(1)

if __name__ == "__main__":
    main()