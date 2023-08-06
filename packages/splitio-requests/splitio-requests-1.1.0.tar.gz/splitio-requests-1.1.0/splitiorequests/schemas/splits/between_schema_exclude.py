# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_load, post_dump, EXCLUDE

from splitiorequests.models.splits.between import Between


class BetweenSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    from_number = fields.Int(data_key='from', required=True)
    to = fields.Int(required=True)

    @post_load
    def load_between(self, data, **kwargs):
        return Between(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
