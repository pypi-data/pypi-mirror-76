# -*- coding: utf-8 -*-


from typing import Optional, List, Dict, Union

from splitiorequests.models.environments.environment import Environment
from splitiorequests.schemas.environments import environment_schema, environment_schema_exclude
from splitiorequests.common.utils import Utils


def load_environment(data: dict, unknown_handler: str = 'RAISE') -> Optional[Environment]:
    loaded_environment = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_environment = environment_schema.EnvironmentSchema().load(data)
    elif handler == "exclude":
        loaded_environment = environment_schema_exclude.EnvironmentSchemaExclude().load(data)
    return loaded_environment


def dump_environment(environment_obj: Environment) -> dict:
    dumped_environment = environment_schema.EnvironmentSchema().dump(environment_obj)
    return dumped_environment


def load_environments(
        data: List[Dict[str, Union[str, bool]]],
        unknown_handler: str = 'RAISE'
) -> Optional[List[Environment]]:
    loaded_environments = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_environments = environment_schema.EnvironmentSchema(many=True).load(data)
    elif handler == "exclude":
        loaded_environments = environment_schema_exclude.EnvironmentSchemaExclude(many=True).load(data)
    return loaded_environments


def dump_environments(environments_obj: List[Environment]) -> dict:
    dumped_environments = environment_schema.EnvironmentSchema(many=True).dump(environments_obj)
    return dumped_environments
