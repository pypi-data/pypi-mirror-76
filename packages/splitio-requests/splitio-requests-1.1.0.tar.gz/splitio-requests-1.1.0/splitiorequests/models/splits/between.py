# -*- coding: utf-8 -*-


from dataclasses import dataclass


@dataclass
class Between:
    from_number: int
    to: int
