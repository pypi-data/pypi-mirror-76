# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import List


@dataclass
class Depends:
    splitName: str
    treatments: List[str]
