import streamlit as st
import pandas as pd
import json
import os

# Set page configuration
st.set_page_config(page_title="Redrob AI Ranker Sandbox", page_icon="🚀", layout="centered")

st.title("🚀 Intelligent Candidate Discovery Sandbox")
st.write("This sandbox environment verifies the end-to-end multi-stage ranking pipeline using a lightweight sample dataset ($\le 100$ profiles) to satisfy Section 10.5 compliance.")

# 1. Provide an option for judges to view or reset the sample data
st.subheader("📦 Evaluation Sample Dataset")

# Inline sample data to ensure it runs out-of-the-box on Streamlit Cloud
sample_candidates = [
    {
        "candidate_id": "CAND_0000001",
        "profile": {"headline": "Senior AI Engineer", "summary": "Python and vector databases", "years_of_experience": 7},
        "skills": [{"name": "Python", "proficiency": "expert"}, {"name": "Vector Database", "proficiency": "expert"}],
        "career_history": [{"company": "SaaS Product Corp", "title": "AI Engineer", "description": "Built neural retrieval pipelines"}],
        "redrob_signals": {"open_to_work_flag": True, "recruiter_response_rate": 0.95, "github_activity_score": 85, "notice_period_days": 15, "interview_completion_rate": 0.9, "profile_completeness_score": 95}
    },
    {
        "candidate_id": "CAND_0000002",
        "profile": {"headline": "Backend Developer", "summary": "Django and Node.js systems", "years_of_experience": 5},
        "skills": [{"name": "Python", "proficiency": "intermediate"}, {"name": "Django", "proficiency": "expert"}],
        "career_history": [{"company": "Tech Solutions", "title": "Backend Dev", "description": "Maintained database servers"}],
        "redrob_signals": {"open_to_work_flag": False, "recruiter_response_rate": 0.70, "github_activity_score": 40, "notice_period_days": 45, "interview_completion_rate": 0.8, "profile_completeness_score": 80}
    },
    {
        "candidate_id": "CAND_0000003",
        "profile": {"headline": "Honeypot Profile Example", "summary": "Fake expert profile", "years_of_experience": 0},
        "skills": [{"name": "Python", "proficiency": "expert"}, {"name": "FAISS", "proficiency": "expert"}],
        "career_history": [],
        "redrob_signals": {"open_to_work_flag": True, "recruiter_response_rate": 0.10, "github_activity_score": -1, "notice_period_days": 90, "interview_completion_rate": 0.2, "profile_completeness_score": 30}
    }
]

# Write data out seamlessly behind the scenes
os.makedirs("data", exist_ok=True)
with open("data/candidates.jsonl", "w") as f:
    for cand in sample_candidates:
        f.write(json.dumps(cand) + "\n")

st.info("💡 A compliant validation sample containing normal candidates and 1 honeypot has been successfully initialized at `data/candidates.jsonl`.")

# 2. Execution Layer
st.subheader("⚙️ Execute Multi-Stage Pipeline")
if st.button("Run Ranker Engine", type="primary"):
    with st.spinner("Executing dense retrieval matrix, honeypot filters, and reasoning generator..."):
        # Run your main pipeline code using terminal execution arguments
        # Replace 'team_xxx.csv' with your actual team file name if preferred
        exit_code = os.system("python main.py --candidates ./data/candidates.jsonl --out ./output/sandbox_submission.csv")
        
        if exit_code == 0 and os.path.exists("output/sandbox_submission.csv"):
            st.success("✅ Pipeline Execution Succeeded!")
            
            # Read and show output back to the judges
            result_df = pd.read_csv("output/sandbox_submission.csv")
            st.dataframe(result_df, use_container_width=True)
        else:
            st.error("❌ Pipeline execution failed. Please verify local path parameters and main.py argument handling.")