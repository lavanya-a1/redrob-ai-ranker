from docx import Document
import re


class JDParser:

    def __init__(self, jd_path):

        self.jd_path = jd_path
        self.text = self.load_document()

    # ---------------------------------
    # Read DOCX
    # ---------------------------------

    def load_document(self):

        doc = Document(self.jd_path)

        paragraphs = []

        for para in doc.paragraphs:

            txt = para.text.strip()

            if txt:

                paragraphs.append(txt.lower())

        return "\n".join(paragraphs)

    # ---------------------------------
    # Experience
    # ---------------------------------

    def extract_experience(self):

        pattern = r"(\d+)\s*[-–]\s*(\d+)\s*years"

        match = re.search(pattern, self.text)

        if match:

            return (
                int(match.group(1)),
                int(match.group(2))
            )

        return None

    # ---------------------------------
    # Skill Extraction
    # ---------------------------------

    def find_keywords(self, keywords):

        found = []

        for word in keywords:

            if re.search(
                rf"\b{re.escape(word.lower())}\b",
                self.text
            ):

                found.append(word)

        return found

    # ---------------------------------
    # Must Have
    # ---------------------------------

    def extract_must_have(self):

        skills = [

            "python",

            "embeddings",

            "retrieval",

            "ranking",

            "llm",

            "fine-tuning",

            "vector database",

            "faiss",

            "milvus",

            "pinecone",

            "qdrant",

            "weaviate",

            "elasticsearch",

            "opensearch",

            "sentence-transformers",

            "bge",

            "e5",

            "evaluation",

            "ndcg",

            "mrr",

            "map"

        ]

        return self.find_keywords(skills)

    # ---------------------------------
    # Nice To Have
    # ---------------------------------

    def extract_nice_to_have(self):

        skills = [

            "lora",

            "qlora",

            "peft",

            "learning-to-rank",

            "xgboost",

            "distributed systems",

            "marketplace",

            "open-source",

            "hr-tech"

        ]

        return self.find_keywords(skills)

    # ---------------------------------
    # Locations
    # ---------------------------------

    def extract_locations(self):

        locations = [

            "pune",

            "noida",

            "hyderabad",

            "mumbai",

            "delhi",

            "delhi ncr"

        ]

        return self.find_keywords(locations)

    # ---------------------------------
    # Behaviour
    # ---------------------------------

    def extract_behavior(self):

        behavior = []

        if "open to work" in self.text:
            behavior.append("open_to_work")

        if "response rate" in self.text:
            behavior.append("good_response")

        if "notice period" in self.text:
            behavior.append("short_notice")

        if "logged in" in self.text:
            behavior.append("recent_activity")

        return behavior

    # ---------------------------------
    # Disqualifiers
    # ---------------------------------

    def extract_disqualifiers(self):

        disqualifiers = [

            "pure research",

            "langchain",

            "consulting firms",

            "computer vision",

            "speech",

            "robotics",

            "framework enthusiasts"

        ]

        return self.find_keywords(
            disqualifiers
        )

    # ---------------------------------
    # Parse Everything
    # ---------------------------------

    def parse(self):

        return {

            "experience":

                self.extract_experience(),

            "must_have":

                self.extract_must_have(),

            "nice_to_have":

                self.extract_nice_to_have(),

            "locations":

                self.extract_locations(),

            "behavior":

                self.extract_behavior(),

            "disqualifiers":

                self.extract_disqualifiers()

        }


# ---------------------------------
# Testing
# ---------------------------------

if __name__ == "__main__":

    parser = JDParser(
        "data/job_description.docx"
    )

    jd = parser.parse()

    print()

    for key, value in jd.items():

        print(key)

        print(value)

        print()