import json
import pandas as pd
from tqdm import tqdm

INPUT_FILE = "data/candidates.jsonl"

rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    for line in tqdm(f):

        candidate = json.loads(line)

        profile = candidate["profile"]

        skills = candidate["skills"]

        career = candidate["career_history"]

        education = candidate["education"]

        signals = candidate["redrob_signals"]

        skill_names = [s["name"] for s in skills]

        career_text = " ".join(
            [job["title"] + " " + job["description"] for job in career]
        )

        education_text = " ".join(
            [edu["degree"] + " " + edu["field_of_study"] for edu in education]
        )

        combined_text = f"""
        {profile['headline']}

        {profile['summary']}

        {career_text}

        {' '.join(skill_names)}

        {education_text}
        """

        rows.append({

            "candidate_id": candidate["candidate_id"],

            "combined_text": combined_text,

            "skills": skill_names,

            "years_exp": profile["years_of_experience"],

            "current_title": profile["current_title"],

            "industry": profile["current_industry"],

            "open_to_work": signals["open_to_work_flag"],

            "github_score": signals["github_activity_score"],

            "notice_period": signals["notice_period_days"],

            "response_rate": signals["recruiter_response_rate"]

        })

df = pd.DataFrame(rows)

print(df.head())

df.to_parquet("data/processed_candidates.parquet")

print("Saved Successfully")