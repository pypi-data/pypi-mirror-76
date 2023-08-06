# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_dump, post_load, EXCLUDE

from splitiorequests.models.workspaces.workspace import Workspace


class WorkspaceSchemaExclude(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.Str(required=True)
    wsid = fields.Str(required=True, data_key='id')

    @post_load
    def load_workspace(self, data, **kwargs):
        return Workspace(**data)

    @post_dump
    def return_dict(self, data, **kwargs):
        return dict(data)
