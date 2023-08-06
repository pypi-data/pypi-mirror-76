# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, post_load, post_dump

from .workspace_schema import WorkspaceSchema
from splitiorequests.models.workspaces.workspaces import Workspaces


class WorkspacesSchema(Schema):
    class Meta:
        ordered = True

    objects = fields.List(fields.Nested(WorkspaceSchema), required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    totalCount = fields.Int(required=True)

    @post_load
    def load_split_definitions(self, data, **kwargs):
        return Workspaces(**data)

    @post_dump
    def convert_to_dict(self, data, **kwargs):
        return dict(data)
