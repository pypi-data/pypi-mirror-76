# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import List

from .condition import Condition
from .bucket import Bucket


@dataclass
class Rule:
    buckets: List[Bucket]
    condition: Condition
