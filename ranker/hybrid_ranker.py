import pandas as pd
import numpy as np
import json
import re

# -------------------------------------------------------------
# 1. Component Scoring Functions
# -------------------------------------------------------------

def compute_experience_score(profile_text):
    """
    Extracts numerical years of experience from profile text 
    and scores it. Target: 5-9 years gets maximum points.
    """
    text = str(profile_text).lower()
    # Corrected regex pattern to safely match things like "5 years" or "5+ years"
    matches = re.findall(r'(\d+)\s*(?:\+)?\s*year', text)
    if matches:
        try:
            exp = max([int(m) for m in matches])
        except ValueError:
            exp = 4 # default fallback
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
    
    score = 0.5 # baseline
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
    
    # 1. Open to work flag (Max 0.30)
    if sig.get('open_to_work_flag') is True:
        score += 0.30
        
    # 2. Recruiter response rate (Max 0.30)
    response_rate = sig.get('recruiter_response_rate', 0.5)
    score += float(response_rate) * 0.30
    
    # 3. GitHub activity score (Max 0.20) - handles -1 baseline safely
    github = sig.get('github_activity_score', -1)
    if github > 0:
        score += min(github / 100, 1) * 0.20
        
    # 4. Notice period adjustment (Max 0.20)
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

print("Processing strategic recruiter scores...")
final_candidates = []

for idx, row in df.iterrows():
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
    
    # No retrieval/search/ranking experience
    if not any(kw in history_text or kw in skills_text for kw in ['retrieval', 'search', 'ranking', 'recommendation']):
        penalties += 0.15
        
    # No vector DB experience
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
        "behavior_score": round(behavior_score, 3)
    })

# Convert to DataFrame, sort, and slice top 100
ranked_df = pd.DataFrame(final_candidates)
ranked_df = ranked_df.sort_values(by="final_score", ascending=False)
top_100 = ranked_df.head(100)

# Save output
top_100.to_csv("output/final_ranked_candidates.csv", index=False)
print("Advanced Hybrid Ranking Complete!")
print(top_100.head(10))