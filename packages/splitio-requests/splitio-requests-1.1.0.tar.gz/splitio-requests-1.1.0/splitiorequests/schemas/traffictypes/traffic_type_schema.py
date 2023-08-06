# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load

from splitiorequests.models.traffictypes.traffic_type import TrafficType


class TrafficTypeSchema(Schema):
    class Meta:
        ordered = True

    name = fields.Str(required=True)
    traffic_type_id = fields.Str(required=True, data_key='id')
    displayAttributeId = fields.Str(required=True)

    @post_load
    def load_traffic_type(self, data, **kwargs):
        return TrafficType(**data)

    @post_dump
    def return_dict(self, data, **kwargs):
        return dict(data)
