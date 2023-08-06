# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE

from .tag_schema_exclude import TagSchemaExclude
from .traffic_type_schema_exclude import TrafficTypeSchemaExclude
from splitiorequests.models.splits.split import Split


class SplitSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    description = fields.Str(missing=None)
    trafficType = fields.Nested(TrafficTypeSchemaExclude)
    creationTime = fields.Integer()
    tags = fields.List(fields.Nested(TagSchemaExclude), missing=None)

    @post_load
    def load_split(self, data, **kwargs):
        return Split(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if key != 'tags' and key != 'description' and data[key] is None):
            del new_data[field_key]
        return dict(new_data)
