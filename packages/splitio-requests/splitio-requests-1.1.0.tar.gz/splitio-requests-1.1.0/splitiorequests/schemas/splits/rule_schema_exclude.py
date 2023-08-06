# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE

from .bucket_schema_exclude import BucketSchemaExclude
from .condition_schema_exclude import ConditionSchemaExclude
from splitiorequests.models.splits.rule import Rule


class RuleSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    buckets = fields.List(fields.Nested(BucketSchemaExclude), required=True)
    condition = fields.Nested(ConditionSchemaExclude, required=True)

    @post_load
    def load_rule(self, data, **kwargs):
        return Rule(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
