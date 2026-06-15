import json
import pandas as pd
from tqdm import tqdm
import argparse
import os

def build_embedding_text(candidate):
    profile = candidate.get("profile", {})
    text = ""

    # Profile
    text += profile.get("headline", "") + " "
    text += profile.get("summary", "") + " "
    text += profile.get("current_title", "") + " "
    text += profile.get("current_industry", "") + " "

    # Career
    for job in candidate.get("career_history", []):
        text += job.get("title", "") + " "
        text += job.get("industry", "") + " "
        text += job.get("description", "") + " "

    # Skills
    for skill in candidate.get("skills", []):
        text += skill.get("name", "") + " "
        text += skill.get("proficiency", "") + " "

    # Education
    for edu in candidate.get("education", []):
        text += edu.get("degree", "") + " "
        text += edu.get("field_of_study", "") + " "

    return text.lower()


def load_candidates(path):
    rows = []
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw candidate file not found at path: {path}")

    print(f"Reading raw profiles from: {path}")
    with open(path, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            candidate = json.loads(line)
            
            # Pre-calculate explicit honeypot detection items to ensure clean type parsing downstream
            skills = candidate.get("skills", [])
            expert_skills_count = sum(1 for s in skills if "expert" in str(s.get("proficiency", "")).lower())
            
            rows.append({
                "candidate_id": candidate["candidate_id"],
                "embedding_text": build_embedding_text(candidate),
                "profile": str(candidate.get("profile", "")),
                "career_history": str(candidate.get("career_history", "")),
                "skills": str(skills),
                "education": str(candidate.get("education", "")),
                "redrob_signals": json.dumps(candidate.get("redrob_signals", {})),
                
                # --- HACKATHON HONEYPOT SANITY PASSES ---
                "experience": float(candidate.get("profile", {}).get("years_of_experience", 0)),
                "expert_skills_count": int(expert_skills_count),
                "raw_career_history": candidate.get("career_history", []) # Kept as object for inline list handling
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Handle incoming execution CLI arguments forwarded by main.py
    parser = argparse.ArgumentParser(description="Preprocess raw jsonl files into structured tables.")
    parser.add_argument('--candidates', type=str, default="data/candidates.jsonl", help="Input file path")
    args = parser.parse_args()

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    df = load_candidates(args.candidates)

    # Save data
    output_path = "data/processed_candidates.parquet"
    df.to_parquet(output_path, index=False)

    print(df.head(2))
    print(f"\n✅ Saved processed data structures to: {output_path}")