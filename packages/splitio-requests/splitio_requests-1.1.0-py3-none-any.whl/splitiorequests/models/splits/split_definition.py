# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import Optional, List

from .treatment import Treatment
from .default_rule import DefaultRule
from .environment import Environment
from .traffic_type import TrafficType
from .rule import Rule


@dataclass
class SplitDefinition:
    treatments: List[Treatment]
    defaultTreatment: str
    defaultRule: List[DefaultRule]
    name: Optional[str] = None
    environment: Optional[Environment] = None
    trafficType: Optional[TrafficType] = None
    killed: Optional[bool] = None
    baselineTreatment: Optional[str] = None
    trafficAllocation: Optional[int] = None
    rules: Optional[List[Rule]] = None
    creationTime: Optional[int] = None
    lastUpdateTime: Optional[int] = None
    comment: Optional[str] = None
