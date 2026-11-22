"""Seed the 46 AI/ML learning briefs from aiml_project.md.

Thirty learning projects already exist as resume or hackathon briefs. This pack
reuses their summaries, approaches and build guides, removes the track-specific
kits, and adds learning concepts plus the documented difficulty. The other
sixteen projects are defined in ``aiml_learning_details``.
"""

from copy import deepcopy

from app.seed.aiml_learning_details import (
    DIFFICULTIES,
    LEARNING_CONCEPTS,
    LEARNING_ONLY,
    TITLES,
)
from app.seed.runner import seed_problems
from app.seed.seed_aiml_hackathon_projects import PROBLEMS as HACKATHON_PROBLEMS
from app.seed.seed_aiml_projects import PROBLEMS as RESUME_PROBLEMS


PROJECT_NUMBERS = [
    8,
    26,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    1,
    4,
    7,
    10,
    14,
    16,
    18,
    21,
    22,
    24,
    25,
    27,
    37,
    38,
    40,
    43,
    44,
    45,
    9,
    12,
    13,
    15,
    17,
    19,
    20,
    23,
    28,
    29,
    39,
    41,
    42,
    46,
    47,
    48,
    49,
    50,
    51,
]

_RESUME_BY_TITLE = {problem["title"]: problem for problem in RESUME_PROBLEMS}
_HACKATHON_BY_TITLE = {problem["title"]: problem for problem in HACKATHON_PROBLEMS}


def _base_problem(number: int) -> dict:
    if number in LEARNING_ONLY:
        return deepcopy(LEARNING_ONLY[number])

    title = TITLES[number]
    problem = _RESUME_BY_TITLE.get(title) or _HACKATHON_BY_TITLE[title]
    return deepcopy(problem)


def _compose(number: int) -> dict:
    problem = _base_problem(number)
    problem.pop("resume_kit", None)
    problem.pop("team_plan", None)
    problem.pop("pitch_guide", None)
    problem["source_id"] = (
        f"manabi-aiml-learning-{PROJECT_NUMBERS.index(number) + 1:03d}"
    )
    problem["goal"] = "learning"
    problem["difficulty"] = DIFFICULTIES[number]
    problem["learning_concepts"] = deepcopy(LEARNING_CONCEPTS[number])
    problem["source_note"] = "Curated AI/ML learning project."
    return problem


PROBLEMS = [_compose(number) for number in PROJECT_NUMBERS]


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
