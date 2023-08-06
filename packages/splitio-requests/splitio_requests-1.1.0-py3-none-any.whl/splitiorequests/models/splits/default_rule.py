# -*- coding: utf-8 -*-


from dataclasses import dataclass


@dataclass
class DefaultRule:
    treatment: str
    size: int
