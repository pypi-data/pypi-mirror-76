# -*- coding: utf-8 -*-


from typing import Optional, List, Dict

from splitiorequests.models.tags.tags import Tags
from splitiorequests.schemas.tags import tags_schema, tags_schema_exclude
from splitiorequests.common.utils import Utils


def load_tags(data: List[Dict[str, str]], unknown_handler: str = 'RAISE') -> Optional[List[Tags]]:
    loaded_tags = None
    handler = Utils.get_unknown_field_handler(unknown_handler)
    if handler == "raise":
        loaded_tags = tags_schema.TagsSchema().load(data)
    elif handler == "exclude":
        loaded_tags = tags_schema_exclude.TagsSchemaExclude().load(data)
    return loaded_tags


def dump_tags(tags_obj: List[Tags]) -> dict:
    dumped_tags = tags_schema.TagsSchema().dump(tags_obj)
    return dumped_tags
