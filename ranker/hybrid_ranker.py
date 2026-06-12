import pandas as pd


# Score Experience

def experience_score(exp):

    if 5 <= exp <= 9:
        return 1.0

    elif 4 <= exp <= 10:
        return 0.8

    return 0.3


# Behavioral Score

def behavioral_score(row):

    score = 0

    if row["open_to_work"]:
        score += 0.30

    score += row["response_rate"] * 0.30

    score += min(row["github_score"] / 100, 1) * 0.20

    if row["notice_period"] <= 30:
        score += 0.20

    return score

# Final Hybrid Score

def calculate_score(row):

    semantic = row["semantic_score"]

    exp = experience_score(row["years_exp"])

    behavior = behavioral_score(row)

    score = (
        0.65 * semantic
        + 0.20 * exp
        + 0.15 * behavior
    )

    return score

# Load Top500

df = pd.read_csv(
    "output/top500_semantic.csv"
)

df["final_score"] = df.apply(
    calculate_score,
    axis=1
)

df = df.sort_values(
    by="final_score",
    ascending=False
)

df.to_csv(
    "output/final_ranked_candidates.csv",
    index=False
)

print(df.head(20))