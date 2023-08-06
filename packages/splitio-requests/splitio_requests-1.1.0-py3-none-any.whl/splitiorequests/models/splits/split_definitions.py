# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import List

from .split_definition import SplitDefinition


@dataclass
class SplitDefinitions:
    objects: List[SplitDefinition]
    offset: int
    limit: int
    totalCount: int
