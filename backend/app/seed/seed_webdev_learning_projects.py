"""Seed the 31 Web Dev learning briefs from webdev_projects.md.

Twenty-four learning projects already exist as resume or hackathon briefs. This
pack reuses their curated summaries, approaches and build guides, removes the
track-specific kits, and adds learning concepts plus the documented difficulty.
The other seven projects are defined in ``webdev_learning_details``.
"""

from copy import deepcopy

from app.seed.runner import seed_problems
from app.seed.seed_webdev_hackathon_projects import PROBLEMS as HACKATHON_PROBLEMS
from app.seed.seed_webdev_projects import PROBLEMS as RESUME_PROBLEMS
from app.seed.webdev_learning_details import (
    DIFFICULTIES,
    LEARNING_CONCEPTS,
    LEARNING_ONLY,
    TITLES,
)


PROJECT_NUMBERS = [
    1,
    2,
    3,
    4,
    7,
    9,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
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
        f"manabi-web-learning-{PROJECT_NUMBERS.index(number) + 1:03d}"
    )
    problem["goal"] = "learning"
    problem["difficulty"] = DIFFICULTIES[number]
    problem["learning_concepts"] = deepcopy(LEARNING_CONCEPTS[number])
    problem["source_note"] = "Curated web development learning project."
    return problem


PROBLEMS = [_compose(number) for number in PROJECT_NUMBERS]


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
