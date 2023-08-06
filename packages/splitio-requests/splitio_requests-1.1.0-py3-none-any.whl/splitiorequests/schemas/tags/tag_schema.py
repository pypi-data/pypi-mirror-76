# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load

from splitiorequests.models.tags.tag import Tag


class TagSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str(required=True)
    objectType = fields.Str(required=True)
    objectName = fields.Str(required=True)

    @post_load
    def load_tag(self, data, **kwargs):
        return Tag(**data)

    @post_dump
    def return_dict(self, data, **kwargs):
        return dict(data)
