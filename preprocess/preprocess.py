import json
import pandas as pd
from tqdm import tqdm


def build_embedding_text(candidate):

    profile = candidate["profile"]

    text = ""

    # Profile

    text += profile["headline"] + " "

    text += profile["summary"] + " "

    text += profile["current_title"] + " "

    text += profile["current_industry"] + " "

    # Career

    for job in candidate["career_history"]:

        text += job["title"] + " "

        text += job["industry"] + " "

        text += job["description"] + " "

    # Skills

    for skill in candidate["skills"]:

        text += skill["name"] + " "

        text += skill["proficiency"] + " "

    # Education

    for edu in candidate["education"]:

        text += edu["degree"] + " "

        text += edu["field_of_study"] + " "

    return text.lower()


def load_candidates(path):

    rows = []

    with open(path, "r", encoding="utf-8") as f:

        for line in tqdm(f):

            candidate = json.loads(line)

            rows.append({

                "candidate_id":

                    candidate["candidate_id"],

                "embedding_text":

                    build_embedding_text(candidate),

                "profile":

                    candidate["profile"],

                "career_history":

                    candidate["career_history"],

                "skills":

                    candidate["skills"],

                "education":

                    candidate["education"],

                "redrob_signals":

                    candidate["redrob_signals"]

            })

    return pd.DataFrame(rows)


if __name__ == "__main__":

    df = load_candidates(

        "data/candidates.jsonl"

    )

    df.to_parquet(

        "data/processed_candidates.parquet",

        index=False

    )

    print(df.head())

    print()

    print("Saved processed_candidates.parquet")