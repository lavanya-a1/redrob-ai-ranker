from preprocess.preprocess import *

candidates = load_candidates("data/candidates.jsonl")

print(len(candidates))

print()

print(build_candidate_text(candidates[0]))