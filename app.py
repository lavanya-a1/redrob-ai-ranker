import streamlit as st
import pandas as pd
import json
import subprocess
import os
import sys

# Set page configuration
st.set_page_config(page_title="Solo Sprint - Ranker Sandbox", page_icon="🚀", layout="wide")

st.title("🚀 Team Solo Sprint: Intelligent Candidate Discovery Sandbox")
st.write("This sandbox environment verifies our end-to-end multi-stage ranking pipeline using a lightweight sample dataset to satisfy Section 10.5 compliance.")

# 1. Setup Data Paths
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# 2. Provide an option for judges to view the sample data
st.subheader("📦 Evaluation Sample Dataset")

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
with open("data/candidates.jsonl", "w", encoding="utf-8") as f:
    for cand in sample_candidates:
        f.write(json.dumps(cand) + "\n")

st.info("💡 Evaluation mock data containing standard candidates and 1 honeypot profile has been automatically initialized at `data/candidates.jsonl`.")

# Expandable view for judges to inspect the raw incoming profiles
with st.expander("🔍 View Raw Input Mock Data (JSONL Format)"):
    st.json(sample_candidates)

st.markdown("---")

# 3. Execution Layer
st.subheader("⚙️ Execute Multi-Stage Pipeline")
st.write("Clicking below invokes our complete matching infrastructure: Preprocessing ➡️ FAISS Vector Generation ➡️ Honeypot Scrubbing ➡️ Rank Assignment ➡️ Structural Validation Check.")

target_output_path = os.path.join("output", "solo_sprint.csv")

if st.button("Run Ranker Engine", type="primary"):
    with st.spinner("Running engine metrics..."):
        try:
            # Using subprocess instead of os.system for reliable, secure execution tracking
            result = subprocess.run(
                [sys.executable, "main.py", "--candidates", "./data/candidates.jsonl", "--out", target_output_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # If successful, read output back to the judges
            if os.path.exists(target_output_path):
                st.success("✅ Pipeline Execution & Verification Succeeded!")
                
                # Render standard system logging output for full transparency
                with st.expander("📋 View Terminal Logs"):
                    st.code(result.stdout)
                
                # Show results data frame
                st.subheader("🏆 Pipeline Ranking Output Results")
                result_df = pd.read_csv(target_output_path)
                st.dataframe(result_df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ Process ran, but the expected output submission file was not generated.")
                
        except subprocess.CalledProcessError as e:
            st.error("❌ Pipeline execution encountered a runtime or structural validation error.")
            with st.expander("⚠️ View Error Logs"):
                st.code(e.stderr if e.stderr else e.stdout)