"""Plain-language copy for the MANABI Web Dev packs."""

from .part_01 import OVERRIDES as PART_01
from .part_02 import OVERRIDES as PART_02
from .part_03 import OVERRIDES as PART_03
from .part_04 import OVERRIDES as PART_04
from .part_05 import OVERRIDES as PART_05
from .part_06 import OVERRIDES as PART_06
from .part_07 import OVERRIDES as PART_07
from .part_08 import OVERRIDES as PART_08

OVERRIDES = {
    **PART_01,
    **PART_02,
    **PART_03,
    **PART_04,
    **PART_05,
    **PART_06,
    **PART_07,
    **PART_08,
}


def apply_plain_language(problems: list[dict]) -> list[dict]:
    for problem in problems:
        override = OVERRIDES.get(problem["source_id"])
        if override:
            problem.update(override)
    return problems
