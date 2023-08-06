# -*- coding: utf-8 -*-


import logging
from typing import Dict, Optional, Union, NoReturn, Iterator
from requests import Response, Session


log = logging.getLogger('splitiorequests')


class WorkspacesResponse:
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


class WorkspacesRequests:
    def __init__(self, headers: Dict[str, str], hostname: str, session: Session) -> None:
        self.__hostname = f"{hostname}/workspaces"
        self.__headers = {**headers, **{'Content-Type': 'application/json'}}
        self.__session = session

    def __method_scope_headers_update(self, new_headers: Dict[str, str]) -> Dict[str, str]:
        updated_headers = {**self.__headers, **new_headers}
        return updated_headers

    def __list_workspaces_chunk(
            self,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> WorkspacesResponse:
        log.info("Getting workspaces")
        get_resp = self.__session.get(
            f'{self.__hostname}?limit={limit}&offset={offset}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return WorkspacesResponse(get_resp)

    def get_workspaces(
            self,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> Union[NoReturn, Iterator[WorkspacesResponse]]:
        if limit < 1 or limit > 50:
            raise ValueError("Limit should be greater than or equal to 1 and less than or equal to 50")

        if offset < 0:
            raise ValueError("Offset should be greater than or equal to 0")

        workspaces = self.__list_workspaces_chunk(offset, limit, headers)

        if not workspaces:
            log.error("Couldn't get workspaces")
            yield workspaces
            return
        else:
            yield workspaces

        workspaces_payload = workspaces.json()
        if workspaces_payload['totalCount'] > workspaces_payload['limit']:
            while workspaces_payload['offset'] < workspaces_payload['totalCount']:
                offset += limit
                workspaces = self.__list_workspaces_chunk(offset, limit, headers)
                if workspaces is None:
                    log.error("Couldn't get workspaces")
                    yield workspaces
                    return
                else:
                    yield workspaces
                workspaces_payload = workspaces.json()
