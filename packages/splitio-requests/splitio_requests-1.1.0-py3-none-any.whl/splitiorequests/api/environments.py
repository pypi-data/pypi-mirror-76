# -*- coding: utf-8 -*-


import logging
import jsonpatch
from typing import Dict, Optional, Union, NoReturn
from requests import Response, Session


log = logging.getLogger('splitiorequests')


class EnvironmentsResponse:
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


class EnvironmentsRequests:
    def __init__(self, headers: Dict[str, str], hostname: str, session: Session) -> None:
        self.__hostname = f"{hostname}/environments"
        self.__headers = {**headers, **{'Content-Type': 'application/json'}}
        self.__session = session

    def __method_scope_headers_update(self, new_headers: Dict[str, str]) -> Dict[str, str]:
        updated_headers = {**self.__headers, **new_headers}
        return updated_headers

    def get_environments(
            self,
            wsid: str,
            headers: Optional[Dict[str, str]] = None
    ) -> EnvironmentsResponse:
        log.info(f"Getting environments from '{wsid}' workspace")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return EnvironmentsResponse(get_resp)

    def create_environment(
            self,
            wsid: str,
            environment_name: str,
            is_production: bool,
            headers: Optional[Dict[str, str]] = None
    ) -> EnvironmentsResponse:
        log.info(f"Creating environment '{environment_name}' in '{wsid}' workspace")
        post_resp = self.__session.post(
            f'{self.__hostname}/ws/{wsid}',
            headers=self.__method_scope_headers_update(headers or {}),
            json={"name": environment_name, "production": is_production}
        )

        return EnvironmentsResponse(post_resp)

    def delete_environment(
            self,
            wsid: str,
            environment_name_or_id: str,
            headers: Optional[Dict[str, str]] = None
    ) -> EnvironmentsResponse:
        log.info(f"Deleting environment '{environment_name_or_id}' from '{wsid}' workspace")
        delete_resp = self.__session.delete(
            f'{self.__hostname}/ws/{wsid}/{environment_name_or_id}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return EnvironmentsResponse(delete_resp)

    def update_environment(
            self,
            wsid: str,
            environment_name_or_id: str,
            old_data: Optional[dict] = None,
            new_data: Optional[dict] = None,
            patch_string: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> Union[NoReturn, EnvironmentsResponse]:
        patch_data = None
        if old_data and new_data:
            patch_data = jsonpatch.make_patch(old_data, new_data).to_string()
        elif not patch_string:
            log.warning("Provide serializers for patch")
            raise TypeError

        log.info(f"Updating environment '{environment_name_or_id}' in '{wsid}' workspace")
        patch_resp = self.__session.patch(
            f'{self.__hostname}/ws/{wsid}/{environment_name_or_id}',
            headers=self.__method_scope_headers_update(headers or {}),
            data=patch_string or patch_data
        )

        return EnvironmentsResponse(patch_resp)
