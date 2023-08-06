# -*- coding: utf-8 -*-


from typing import Optional

from splitiorequests.models.workspaces.workspaces import Workspaces
from splitiorequests.schemas.workspaces.workspaces_schema import WorkspacesSchema
from splitiorequests.schemas.workspaces.workspaces_schema_exclude import WorkspacesSchemaExclude
from splitiorequests.common.utils import Utils


def load_workspaces(data: dict, unknown_handler: str = 'RAISE') -> Optional[Workspaces]:
    loaded_workspaces = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_workspaces = WorkspacesSchema().load(data)
    elif handler == "exclude":
        loaded_workspaces = WorkspacesSchemaExclude().load(data)
    return loaded_workspaces


def dump_workspaces(workspaces_obj: Workspaces) -> dict:
    dumped_workspaces = WorkspacesSchema().dump(workspaces_obj)
    return dumped_workspaces
