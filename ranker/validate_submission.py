import pandas as pd
import os

print("--- Running Submission Integrity Check ---")

sub_path = "output/submission.csv"

# 1. File existence check
if not os.path.exists(sub_path):
    print("❌ Error: submission.csv file is missing from output/ directory!")
    exit(1)

df = pd.read_csv(sub_path)

errors = 0

# 2. Check column count and names
expected_cols = ['rank', 'candidate_id']
if list(df.columns) != expected_cols:
    print(f"❌ Error: Columns do not match specification. Expected {expected_cols}, got {list(df.columns)}")
    errors += 1

# 3. Check exact row count
if len(df) != 100:
    print(f"❌ Error: Row count must be exactly 100. Your file has {len(df)} entries.")
    errors += 1

# 4. Check for null or empty values
if df.isnull().any().any():
    print("❌ Error: Missing or NaN values detected inside the submission file!")
    print(df.isnull().sum())
    errors += 1

# 5. Check rank column sequencing
expected_ranks = list(range(1, 101))
if list(df['rank']) != expected_ranks:
    print("❌ Error: The 'rank' column must be sequential from 1 to 100.")
    errors += 1

# 6. Check for duplicate candidate submissions
if df['candidate_id'].duplicated().any():
    print("❌ Error: Duplicate candidate IDs found in your top 100 picks!")
    errors += 1

# Final Verdict
if errors == 0:
    print("✅ Validation Passed! Your submission.csv is perfect and ready to turn in.")
else:
    print(f"❌ Validation Failed with {errors} total layout error(s).")