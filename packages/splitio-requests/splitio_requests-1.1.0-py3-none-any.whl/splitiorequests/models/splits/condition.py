# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import List

from .matcher import Matcher


@dataclass
class Condition:
    combiner: str
    matchers: List[Matcher]
