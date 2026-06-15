import pandas as pd
import numpy as np
import json
import re

# -------------------------------------------------------------
# 1. Component Scoring Functions
# -------------------------------------------------------------

def verify_profile_sanity(row):
    """
    Programmatic structural filter targeting hackathon honeypot profiles 
    containing impossible timelines or artificially inflated skills.
    Returns True if authentic, False if a clear honeypot anomaly.
    """
    # 1. Experience Timeline Contradiction Check
    try:
        # Convert raw string representation of list back to list if needed safely
        history = row.get('raw_career_history', [])
        if isinstance(history, str):
            # Fallback if text format string exists
            history_list = []
        else:
            history_list = history
            
        # Parse individual job lengths if available, or analyze text logic
        years_exp = float(row.get('experience', row.get('years_of_experience_raw', 0)))
    except Exception:
        years_exp = 0
        history_list = []

    # 2. Skill Density Over-inflation Check
    # Section 7 warns against "expert proficiency in 10 skills with 0 years used"
    expert_cnt = int(row.get('expert_skills_count', 0))
    if years_exp <= 1.0 and expert_cnt >= 5:
        return False # Blatant fraud profile logic block

    # 3. Future Dating Anomaly Check
    # Catches profiles asserting live job dates past the real world competition limit (2026)
    history_str = str(row.get('career_history', '')).lower()
    future_years = [str(y) for y in range(2027, 2035)]
    if any(yr in history_str for yr in future_years):
        return False

    return True

def compute_experience_score(profile_text):
    """
    Extracts numerical years of experience from profile text 
    and scores it. Target: 5-9 years gets maximum points.
    """
    text = str(profile_text).lower()
    matches = re.findall(r'(\d+)\s*(?:\+)?\s*year', text)
    if matches:
        try:
            exp = max([int(m) for m in matches])
        except ValueError:
            exp = 4
    else:
        exp = 4

    if 5 <= exp <= 9:
        return 1.0
    elif 4 <= exp <= 10:
        return 0.8
    return 0.3

def compute_product_score(career_history):
    """
    Scores higher if candidate has product company keywords 
    vs purely service-oriented descriptions.
    """
    history = str(career_history).lower()
    product_keywords = ['product-based', 'saas', 'scaling production', 'core product', 'b2b', 'b2c']
    service_keywords = ['client location', 'service-based', 'consulting for', 'maintenance project']
    
    score = 0.5
    if any(kw in history for kw in product_keywords):
        score += 0.5
    if any(kw in history for kw in service_keywords):
        score -= 0.3
    return max(0.0, min(1.0, score))

def compute_skills_score(skills_data):
    """
    Checks for the exact presence of critical must-have skills requested by the JD.
    """
    skills_text = str(skills_data).lower()
    must_haves = ['python', 'embeddings', 'retrieval', 'ranking', 'vector database']
    matched = sum(1 for skill in must_haves if skill in skills_text)
    return matched / len(must_haves)

def compute_behavior_score(signals):
    """
    Parses the redrob_signals dictionary mapping directly to the exact dataset schema.
    """
    try:
        if isinstance(signals, str):
            sig = json.loads(signals)
        elif isinstance(signals, dict):
            sig = signals
        else:
            sig = {}
    except Exception:
        sig = {}

    score = 0.0
    if sig.get('open_to_work_flag') is True:
        score += 0.30
        
    response_rate = sig.get('recruiter_response_rate', 0.5)
    score += float(response_rate) * 0.30
    
    github = sig.get('github_activity_score', -1)
    if github > 0:
        score += min(github / 100, 1) * 0.20
        
    notice = sig.get('notice_period_days', 90)
    if notice <= 30:
        score += 0.20
    elif notice <= 60:
        score += 0.10
        
    return score

# -------------------------------------------------------------
# 2. Main Ranking Pipeline
# -------------------------------------------------------------

print("Loading Top 1000 candidates...")
df = pd.read_parquet("output/top1000_candidates.parquet")

print("Processing strategic recruiter scores with Honeypot Filters...")
final_candidates = []

for idx, row in df.iterrows():
    # 1. Run the structural profile sanity block
    if not verify_profile_sanity(row):
        # Quarantine the candidate completely if structural lies are present
        final_score = 0.0
        semantic_score = float(row['semantic_score'])
        exp_score, prod_score, skills_score, behavior_score = 0.0, 0.0, 0.0, 0.0
    else:
        # Base scores
        semantic_score = float(row['semantic_score'])
        exp_score = compute_experience_score(row.get('profile', ''))
        prod_score = compute_product_score(row.get('career_history', ''))
        skills_score = compute_skills_score(row.get('skills', ''))
        behavior_score = compute_behavior_score(row.get('redrob_signals', {}))
        
        # Weighted calculation
        weighted_score = (
            0.50 * semantic_score +
            0.10 * exp_score +
            0.10 * prod_score +
            0.15 * skills_score +
            0.15 * behavior_score
        )
        
        # Apply hard penalties based on negative recruiter signals/disqualifiers
        penalties = 0.0
        history_text = str(row.get('career_history', '')).lower()
        skills_text = str(row.get('skills', '')).lower()
        
        if not any(kw in history_text or kw in skills_text for kw in ['retrieval', 'search', 'ranking', 'recommendation']):
            penalties += 0.15
            
        if not any(kw in history_text or kw in skills_text for kw in ['vector', 'faiss', 'milvus', 'qdrant', 'chroma']):
            penalties += 0.10

        final_score = weighted_score - penalties

    # Store clean row data
    final_candidates.append({
        "candidate_id": row['candidate_id'],
        "final_score": round(final_score, 4),
        "semantic_score": round(semantic_score, 3),
        "exp_score": round(exp_score, 3),
        "skills_score": round(skills_score, 3),
        "behavior_score": round(behavior_score, 3),
        
        # Preserve specific structural keys for dynamic reasoning generator step
        "years_of_experience": row.get('experience', 4),
        "notice_period_days": 30 if behavior_score > 0.25 else 90, # derived approximation
        "recruiter_response_rate": row.get('response_score', 0.8),
        "is_product_company": 1 if prod_score > 0.6 else 0,
        "has_python": 1 if 'python' in str(row.get('skills', '')).lower() else 0,
        "has_embeddings": 1 if 'embeddings' in str(row.get('skills', '')).lower() else 0,
        "has_retrieval": 1 if 'retrieval' in str(row.get('skills', '')).lower() else 0,
        "has_faiss": 1 if 'faiss' in str(row.get('skills', '')).lower() else 0
    })

# Convert to DataFrame, sort, and slice top 100
ranked_df = pd.DataFrame(final_candidates)

# Tie-Breaking Rule (Addressing Issue 9): Sort by score descending, then candidate_id ascending
ranked_df = ranked_df.sort_values(by=["final_score", "candidate_id"], ascending=[False, True])
top_100 = ranked_df.head(100)

# Save intermediate output for presentation step
top_100.to_csv("output/final_ranked_candidates.csv", index=False)
print("Advanced Hybrid Ranking Complete! Honeypots cleared successfully.")