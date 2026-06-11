def get_skill_names(skills):
    return [skill["name"] for skill in skills]

def get_product_company_score(career_history):

    service_companies = [
        "TCS",
        "Infosys",
        "Wipro",
        "Cognizant",
        "Capgemini",
        "Accenture",
        "Tech Mahindra",
        "HCL"
    ]

    score = 0

    for job in career_history:

        company = job["company"].lower()

        found = False

        for s in service_companies:

            if s.lower() in company:
                found = True

        if not found:
            score += 1

    return score

def get_total_experience(profile):
    return profile["years_of_experience"]

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

def get_behavior_score(signals):

    score = 0

    if signals["open_to_work_flag"]:
        score += 2

    score += signals["recruiter_response_rate"]

    score += signals["interview_completion_rate"]

    score += signals["profile_completeness_score"] / 100

    if signals["github_activity_score"] > 0:
        score += signals["github_activity_score"] / 100

    return score

def get_embedding_text(candidate):

    profile = candidate["profile"]

    text = ""

    text += profile["headline"] + " "

    text += profile["summary"] + " "

    for job in candidate["career_history"]:

        text += job["title"] + " "

        text += job["description"] + " "

    for skill in candidate["skills"]:

        text += skill["name"] + " "

    return text