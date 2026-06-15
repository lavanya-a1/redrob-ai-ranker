# preprocess/feature_builder.py

from typing import List


# -------------------------------------------------
# Skills
# -------------------------------------------------

def get_skill_names(skills: List[dict]):

    return [
        skill["name"].lower()
        for skill in skills
    ]


# -------------------------------------------------
# Product Company Score
# -------------------------------------------------

def get_product_company_score(career_history):

    service_companies = {

        "tcs",
        "infosys",
        "wipro",
        "cognizant",
        "capgemini",
        "accenture",
        "tech mahindra",
        "hcl"

    }

    total = len(career_history)

    if total == 0:
        return 0

    product_count = 0

    for job in career_history:

        company = job["company"].lower()

        if not any(
            s in company
            for s in service_companies
        ):

            product_count += 1

    return product_count / total

# -------------------------------------------------
# Experience
# -------------------------------------------------

def get_total_experience(profile):

    return profile.get(
        "years_of_experience",
        0
    )


# -------------------------------------------------
# Notice Period Score
# -------------------------------------------------

def get_notice_score(signals):

    notice = signals["notice_period_days"]

    if notice <= 30:
        return 1.0

    elif notice <= 60:
        return 0.8

    elif notice <= 90:
        return 0.5

    else:
        return 0.2


# -------------------------------------------------
# Behavior Score
# -------------------------------------------------

def get_behavior_score(signals):

    score = 0

    if signals["open_to_work_flag"]:
        score += 2

    score += (
        signals["recruiter_response_rate"] * 2
    )

    score += (
        signals["interview_completion_rate"] * 2
    )

    score += (
        signals["profile_completeness_score"] / 100
    )

    github = signals["github_activity_score"]

    if github != -1:

        score += github / 100

    return score / 8


# -------------------------------------------------
# Relocation Score
# -------------------------------------------------

def get_relocation_score(signals):

    return int(
        signals["willing_to_relocate"]
    )


# -------------------------------------------------
# Open To Work
# -------------------------------------------------

def get_open_to_work(signals):

    return int(
        signals["open_to_work_flag"]
    )


# -------------------------------------------------
# Response Score
# -------------------------------------------------

def get_response_score(signals):

    return signals[
        "recruiter_response_rate"
    ]


# -------------------------------------------------
# Interview Score
# -------------------------------------------------

def get_interview_score(signals):

    return signals[
        "interview_completion_rate"
    ]


# -------------------------------------------------
# GitHub Score
# -------------------------------------------------

def get_github_score(signals):

    github = signals[
        "github_activity_score"
    ]

    if github == -1:
        return 0

    return github / 100


# -------------------------------------------------
# Candidate Text For Embeddings
# -------------------------------------------------

def get_embedding_text(candidate):

    profile = candidate["profile"]

    text = ""

    # ----------------------

    text += profile["headline"] + " "

    text += profile["summary"] + " "

    text += profile["current_title"] + " "

    text += profile["current_industry"] + " "

    # ----------------------

    for job in candidate["career_history"]:

        text += job["title"] + " "

        text += job["industry"] + " "

        text += job["description"] + " "

    # ----------------------

    for skill in candidate["skills"]:

        text += skill["name"] + " "

        text += skill["proficiency"] + " "

    # ----------------------

    for edu in candidate.get(
        "education",
        []
    ):

        text += edu["degree"] + " "

        text += edu[
            "field_of_study"
        ] + " "

    # ----------------------

    for cert in candidate.get(
        "certifications",
        []
    ):

        text += cert["name"] + " "

    # ----------------------

    return text.lower()


# -------------------------------------------------
# Build Candidate Features
# -------------------------------------------------

def build_candidate_features(candidate):

    return {

        "candidate_id":

            candidate["candidate_id"],

        "skills":

            get_skill_names(
                candidate["skills"]
            ),

        "experience":

            get_total_experience(
                candidate["profile"]
            ),

        "product_company_score":

            get_product_company_score(
                candidate["career_history"]
            ),

        "behavior_score":

            get_behavior_score(
                candidate["redrob_signals"]
            ),

        "notice_score":

            get_notice_score(
                candidate["redrob_signals"]
            ),

        "relocation":

            get_relocation_score(
                candidate["redrob_signals"]
            ),

        "open_to_work":

            get_open_to_work(
                candidate["redrob_signals"]
            ),

        "response_score":

            get_response_score(
                candidate["redrob_signals"]
            ),

        "interview_score":

            get_interview_score(
                candidate["redrob_signals"]
            ),

        "github_score":

            get_github_score(
                candidate["redrob_signals"]
            ),

        "embedding_text":

            get_embedding_text(
                candidate
            )

    }