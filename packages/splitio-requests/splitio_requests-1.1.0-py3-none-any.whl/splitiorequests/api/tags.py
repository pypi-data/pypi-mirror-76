# -*- coding: utf-8 -*-


import logging
from typing import Dict, Optional, List
from requests import Response, Session


log = logging.getLogger('splitiorequests')


class TagsResponse:
    def __init__(self, response: Response) -> None:
        self.url = response.url
        self.status_code = response.status_code
        self.headers = response.headers
        self.json = response.json

    def __bool__(self):
        if self.status_code == 200:
            return True
        else:
            return False


class TagsRequests:
    def __init__(self, headers: Dict[str, str], hostname: str, session: Session) -> None:
        self.__hostname = f"{hostname}/tags"
        self.__headers = {**headers, **{'Content-Type': 'application/json'}}
        self.__session = session

    def __method_scope_headers_update(self, new_headers: Dict[str, str]) -> Dict[str, str]:
        updated_headers = {**self.__headers, **new_headers}
        return updated_headers

    def associate_tags(
            self,
            wsid: str,
            object_name: str,
            object_type: str,
            payload: List[str],
            headers: Optional[Dict[str, str]] = None
    ) -> TagsResponse:
        if object_type != 'Split':
            raise ValueError("Currently only supported object type: Split")

        log.info(f"Associating tags with '{object_name}' '{object_type}' in '{wsid}' workspace")
        post_resp = self.__session.post(
            f'{self.__hostname}/ws/{wsid}/object/{object_name}/objecttype/{object_type}',
            headers=self.__method_scope_headers_update(headers or {}),
            json=payload
        )

        return TagsResponse(post_resp)
