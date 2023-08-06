# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE

from .between_schema_exclude import BetweenSchemaExclude
from .depends_schema_exclude import DependsSchemaExclude
from splitiorequests.models.splits.matcher import Matcher


class MatcherSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    matcher_type = fields.Str(required=True, data_key='type')
    negate = fields.Bool()
    attribute = fields.Str()
    string = fields.Str()
    depends = fields.Nested(DependsSchemaExclude)
    strings = fields.List(fields.Str())
    date = fields.Int()
    between = fields.Nested(BetweenSchemaExclude)
    number = fields.Int()
    bool = fields.Bool()

    @post_load
    def load_matcher(self, data, **kwargs):
        return Matcher(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return dict(new_data)
