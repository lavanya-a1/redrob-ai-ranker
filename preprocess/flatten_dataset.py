import json
import pandas as pd
from tqdm import tqdm

INPUT_FILE = "data/candidates.jsonl"

rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    for line in tqdm(f):

        candidate = json.loads(line)

        profile = candidate["profile"]
        career = candidate["career_history"]
        education = candidate["education"]
        skills = candidate["skills"]
        signals = candidate["redrob_signals"]

        # ----------------------------
        # Career History
        # ----------------------------

        career_text = ""

        for job in career:

            career_text += f"""
            Company: {job['company']}
            Role: {job['title']}
            Industry: {job['industry']}
            Description:
            {job['description']}
            """

        # ----------------------------
        # Education
        # ----------------------------

        education_text = ""

        for edu in education:

            education_text += f"""
            {edu['degree']} in
            {edu['field_of_study']}
            from {edu['institution']}
            """

        # ----------------------------
        # Skills
        # ----------------------------

        skills_text = ""

        for skill in skills:

            skills_text += f"""
            {skill['name']}
            ({skill['proficiency']})
            """

        # ----------------------------
        # Recruiter Summary
        # ----------------------------

        candidate_text = f"""

        Current Role:
        {profile['current_title']}

        Experience:
        {profile['years_of_experience']} years

        Industry:
        {profile['current_industry']}

        Professional Headline:
        {profile['headline']}

        Professional Summary:
        {profile['summary']}

        Career History:
        {career_text}

        Skills:
        {skills_text}

        Education:
        {education_text}

        """

        rows.append({

            "candidate_id": candidate["candidate_id"],

            "candidate_text": candidate_text,

            "summary_text": profile["summary"],

            "career_text": career_text,

            "skills_text": skills_text,

            "education_text": education_text,

            "years_exp": profile["years_of_experience"],

            "current_title": profile["current_title"],

            "industry": profile["current_industry"],

            "location": profile["location"],

            "country": profile["country"],

            "open_to_work": signals["open_to_work_flag"],

            "github_score": signals["github_activity_score"],

            "notice_period": signals["notice_period_days"],

            "response_rate": signals["recruiter_response_rate"],

            "profile_score": signals["profile_completeness_score"],

            "interview_rate": signals["interview_completion_rate"],

            "saved_by_recruiters": signals["saved_by_recruiters_30d"],

            "relocate": signals["willing_to_relocate"],

            "preferred_mode": signals["preferred_work_mode"]

        })

df = pd.DataFrame(rows)

df.to_parquet(
    "data/processed_candidates.parquet",
    index=False
)

print(df.head())

print("Saved Successfully")