
from typing import NamedTuple

import re

RANGE = re.compile(r"(-?\d+)(?:-(-?\d+))?")

class Range(NamedTuple):
    start: int
    end: int

    @staticmethod
    def from_string(range: str) -> "Range":
        m = re.match(RANGE, range)

        start = m.group(1)
        end = m.group(2) or start

        return Range(int(start), int(end))