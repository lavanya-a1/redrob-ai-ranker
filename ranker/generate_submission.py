import pandas as pd
import os

print("Generating final submission file...")

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# 1. Load your final hybrid ranked results
if not os.path.exists("output/final_ranked_candidates.csv"):
    raise FileNotFoundError("Could not find final_ranked_candidates.csv. Please run hybrid_ranker.py first.")

df = pd.read_csv("output/final_ranked_candidates.csv")

# 2. Pick the absolute top 100 candidates
top_100 = df.head(100).copy()

# 3. Create the required sequential ranking column (1 to 100)
top_100['rank'] = range(1, len(top_100) + 1)

# 4. Map to exact submission format columns required by specification
submission_df = top_100[['rank', 'candidate_id']].rename(
    columns={'candidate_id': 'candidate_id'}
)

# 5. Save cleanly to the root or output folder as requested
submission_path = "output/submission.csv"
submission_df.to_csv(submission_path, index=False)

print(f"Success! Final submission file created at: {submission_path}")
print("\nFirst 10 rows of your submission file:")
print(submission_df.head(10))