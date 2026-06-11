import re

def parse_job_description(text):

    jd = {}

    jd["must_have"] = []

    jd["nice_to_have"] = []

    jd["disqualifiers"] = []

    jd["locations"] = []

    jd["experience"] = None

    return jd