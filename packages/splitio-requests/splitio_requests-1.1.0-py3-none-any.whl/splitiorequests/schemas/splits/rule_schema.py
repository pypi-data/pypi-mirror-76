# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_load, post_dump

from .bucket_schema import BucketSchema
from .condition_schema import ConditionSchema
from splitiorequests.models.splits.rule import Rule


class RuleSchema(Schema):
    class Meta:
        ordered = True

    buckets = fields.List(fields.Nested(BucketSchema), required=True)
    condition = fields.Nested(ConditionSchema, required=True)

    @post_load
    def load_rule(self, data, **kwargs):
        return Rule(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
