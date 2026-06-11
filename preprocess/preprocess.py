import json
from tqdm import tqdm


def load_candidates(filepath):
    candidates = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            candidates.append(json.loads(line))

    return candidates

def extract_skill_text(skills):

    names = []

    for skill in skills:
        names.append(skill["name"])

    return " ".join(names)

def extract_career_text(career_history):

    text = ""

    for job in career_history:

        text += job["title"] + " "

        text += job["description"] + " "

    return text

def extract_education_text(education):

    text = ""

    for edu in education:

        text += edu["degree"] + " "

        text += edu["field_of_study"] + " "

    return text

def build_candidate_text(candidate):

    profile = candidate["profile"]

    headline = profile["headline"]

    summary = profile["summary"]

    skills = extract_skill_text(candidate["skills"])

    career = extract_career_text(candidate["career_history"])

    education = extract_education_text(candidate["education"])

    combined = f"""
    {headline}

    {summary}

    {career}

    {skills}

    {education}
    """

    return combined