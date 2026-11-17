"""Seed the 28 AI/ML hackathon briefs from aiml_project.md.

Seventeen hackathon projects already exist as resume briefs. Their curated
facts and build guides are reused here so the two tracks do not drift. Each row
gets a short problem statement, a team plan and a pitch kit. The remaining
eleven projects only exist on the hackathon track and are defined in
``aiml_hackathon_details.py``.
"""

from copy import deepcopy

from app.seed.aiml_hackathon_details import NEW_PROJECTS, STATEMENTS
from app.seed.aiml_hackathon_kits import KITS
from app.seed.runner import seed_problems
from app.seed.seed_aiml_projects import PROBLEMS as RESUME_PROBLEMS


PROJECT_NUMBERS = [
    1,
    2,
    3,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    18,
    19,
    20,
    21,
    23,
    24,
    29,
    31,
    33,
    40,
    41,
    44,
    45,
]

RESUME_SOURCE_IDS = {
    1: "manabi-aiml-resume-001",
    2: "manabi-aiml-resume-002",
    3: "manabi-aiml-resume-003",
    5: "manabi-aiml-resume-005",
    6: "manabi-aiml-resume-006",
    7: "manabi-aiml-resume-007",
    9: "manabi-aiml-resume-008",
    11: "manabi-aiml-resume-009",
    13: "manabi-aiml-resume-010",
    14: "manabi-aiml-resume-011",
    18: "manabi-aiml-resume-012",
    20: "manabi-aiml-resume-013",
    23: "manabi-aiml-resume-014",
    24: "manabi-aiml-resume-015",
    29: "manabi-aiml-resume-018",
    40: "manabi-aiml-resume-021",
    41: "manabi-aiml-resume-022",
}

_RESUME_BY_SOURCE_ID = {
    problem["source_id"]: problem for problem in RESUME_PROBLEMS
}


def _base_problem(number: int) -> dict:
    if number in NEW_PROJECTS:
        return deepcopy(NEW_PROJECTS[number])

    problem = deepcopy(_RESUME_BY_SOURCE_ID[RESUME_SOURCE_IDS[number]])
    problem.pop("resume_kit", None)
    return problem


def _compose(number: int) -> dict:
    problem = _base_problem(number)
    position = PROJECT_NUMBERS.index(number) + 1
    problem["source_id"] = f"manabi-aiml-hackathon-{position:03d}"
    problem["goal"] = "hackathon"
    problem["summary"] = STATEMENTS[number]
    problem["source_note"] = "Curated AI/ML hackathon brief. Check every dataset licence before use."
    problem["team_plan"] = deepcopy(KITS[number]["team_plan"])
    problem["pitch_guide"] = deepcopy(KITS[number]["pitch_guide"])
    return problem


PROBLEMS = [_compose(number) for number in PROJECT_NUMBERS]


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
