# -*- coding: utf-8 -*-


import logging
from typing import Dict, Optional
from requests import Response, Session


log = logging.getLogger('splitiorequests')


class TrafficTypesResponse:
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


class TrafficTypesRequests:
    def __init__(self, headers: Dict[str, str], hostname: str, session: Session) -> None:
        self.__hostname = f"{hostname}/trafficTypes"
        self.__headers = {**headers, **{'Content-Type': 'application/json'}}
        self.__session = session

    def __method_scope_headers_update(self, new_headers: Dict[str, str]) -> Dict[str, str]:
        updated_headers = {**self.__headers, **new_headers}
        return updated_headers

    def get_traffic_types(self, wsid: str, headers: Optional[Dict[str, str]] = None) -> TrafficTypesResponse:
        log.info(f"Getting traffic types from '{wsid}' workspace")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return TrafficTypesResponse(get_resp)
