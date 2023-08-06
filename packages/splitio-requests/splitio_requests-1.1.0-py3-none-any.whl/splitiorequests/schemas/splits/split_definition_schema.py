# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load

from .traffic_type_schema import TrafficTypeSchema
from .rule_schema import RuleSchema
from .treatment_schema import TreatmentSchema
from .default_rule_schema import DefaultRuleSchema
from .environment_schema import EnvironmentSchema
from splitiorequests.models.splits.split_definition import SplitDefinition


class SplitDefinitionSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str()
    environment = fields.Nested(EnvironmentSchema)
    trafficType = fields.Nested(TrafficTypeSchema)
    killed = fields.Bool()
    treatments = fields.List(fields.Nested(TreatmentSchema), required=True)
    defaultTreatment = fields.Str(required=True)
    baselineTreatment = fields.Str()
    trafficAllocation = fields.Int()
    rules = fields.List(fields.Nested(RuleSchema))
    defaultRule = fields.List(fields.Nested(DefaultRuleSchema), required=True)
    creationTime = fields.Int()
    lastUpdateTime = fields.Int()
    comment = fields.Str()

    @post_load
    def load_split_definition(self, data, **kwargs):
        return SplitDefinition(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return dict(new_data)
