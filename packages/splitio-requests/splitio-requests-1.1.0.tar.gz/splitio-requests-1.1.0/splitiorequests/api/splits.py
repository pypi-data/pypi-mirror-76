# -*- coding: utf-8 -*-


import logging
import jsonpatch
from typing import Dict, Optional, Iterator, Union, NoReturn
from requests import Response, Session

log = logging.getLogger('splitiorequests')


class SplitsResponse:
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


class SplitsRequests:
    def __init__(self, headers: Dict[str, str], hostname: str, session: Session) -> None:
        self.__hostname = f"{hostname}/splits"
        self.__headers = {**headers, **{'Content-Type': 'application/json'}}
        self.__session = session

    def __method_scope_headers_update(self, new_headers: Dict[str, str]) -> Dict[str, str]:
        updated_headers = {**self.__headers, **new_headers}
        return updated_headers

    def create_split(
            self,
            wsid: str,
            traffic_type_id_or_name: str,
            payload: dict,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Creating split '{payload.get('name', None)}' in '{wsid}' workspace")
        post_resp = self.__session.post(
            f'{self.__hostname}/ws/{wsid}/trafficTypes/{traffic_type_id_or_name}',
            headers=self.__method_scope_headers_update(headers or {}),
            json=payload
        )
        return SplitsResponse(post_resp)

    def __list_splits_chunk(
            self,
            wsid: str,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Getting list of splits from '{wsid}' workspace - offset: '{offset}' - limit: '{limit}'")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}?limit={limit}&offset={offset}',
            headers=self.__method_scope_headers_update(headers or {})
        )
        return SplitsResponse(get_resp)

    def list_splits(
            self,
            wsid: str,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> Union[NoReturn, Iterator[SplitsResponse]]:
        if limit < 1 or limit > 50:
            raise ValueError("Limit should be greater than or equal to 1 and less than or equal to 50")

        if offset < 0:
            raise ValueError("Offset should be greater than or equal to 0")

        splits = self.__list_splits_chunk(wsid, offset, limit, headers)
        if not splits:
            log.error(f"Couldn't get splits list from '{wsid}' workspace")
            yield splits
            return
        else:
            yield splits

        splits_json = splits.json()
        if splits_json['totalCount'] > splits_json['limit']:
            while splits_json['offset'] < splits_json['totalCount']:
                offset += limit
                splits = self.__list_splits_chunk(wsid, offset, limit)
                if not splits:
                    log.error(f"Couldn't get splits list from '{wsid}' workspace")
                    yield splits
                    return
                else:
                    yield splits
                splits_json = splits.json()

    def get_split(self, split_name: str, wsid: str, headers: Optional[Dict[str, str]] = None) -> SplitsResponse:
        log.info(f"Getting split '{split_name}' from '{wsid}' workspace")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}/{split_name}',
            headers=self.__method_scope_headers_update(headers or {})
        )
        return SplitsResponse(get_resp)

    def delete_split(self, split_name: str, wsid: str, headers: Optional[Dict[str, str]] = None) -> SplitsResponse:
        log.info(f"Deleting split '{split_name}' from '{wsid}' workspace")
        delete_resp = self.__session.delete(
            f'{self.__hostname}/ws/{wsid}/{split_name}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return SplitsResponse(delete_resp)

    def update_split_description(
            self,
            split_name: str,
            wsid: str,
            description: str,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Updating '{split_name}' split description in '{wsid}' workspace")
        put_resp = self.__session.put(
            f'{self.__hostname}/ws/{wsid}/{split_name}/updateDescription',
            headers=self.__method_scope_headers_update(headers or {}),
            data=description
        )

        return SplitsResponse(put_resp)

    def create_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            payload: dict,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Creating '{split_name}' split definition in '{environment_name}' environment")
        post_resp = self.__session.post(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_name}',
            headers=self.__method_scope_headers_update(headers or {}),
            json=payload
        )

        return SplitsResponse(post_resp)

    def get_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Getting '{split_name}' split definition from '{environment_name}' environment")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_name}',
            headers=self.__method_scope_headers_update(headers or {}),
        )

        return SplitsResponse(get_resp)

    def partial_update_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            old_data: Optional[dict] = None,
            new_data: Optional[dict] = None,
            patch_string: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> Union[NoReturn, SplitsResponse]:
        patch_data = None
        if old_data and new_data:
            patch_data = jsonpatch.make_patch(old_data, new_data).to_string()
        elif not patch_string:
            log.error("Provide serializers for patch")
            raise TypeError

        log.info(f"Partially updating '{split_name}' split definition in '{environment_name}' environment")
        patch_resp = self.__session.patch(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_name}',
            headers=self.__method_scope_headers_update(headers or {}),
            data=patch_string or patch_data
        )

        return SplitsResponse(patch_resp)

    def full_update_split_definition_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            payload: dict,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Fully updating '{split_name}' split definition in '{environment_id_or_name}' environment")
        put_resp = self.__session.put(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_id_or_name}',
            headers=self.__method_scope_headers_update(headers or {}),
            json=payload
        )

        return SplitsResponse(put_resp)

    def remove_split_definition_from_environment(
            self,
            split_name: str,
            wsid: str,
            environment_name: str,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Removing '{split_name}' split definition from '{environment_name}' environment")
        delete_resp = self.__session.delete(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_name}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return SplitsResponse(delete_resp)

    def __list_split_definitions_in_environment_chunk(
            self,
            wsid: str,
            environment_name: str,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Getting split definitions from '{environment_name}' environment")
        get_resp = self.__session.get(
            f'{self.__hostname}/ws/{wsid}/environments/{environment_name}?limit={limit}&offset={offset}',
            headers=self.__method_scope_headers_update(headers or {})
        )

        return SplitsResponse(get_resp)

    def list_split_definitions_in_environment(
            self,
            wsid: str,
            environment_name: str,
            offset: int = 0,
            limit: int = 50,
            headers: Optional[Dict[str, str]] = None
    ) -> Union[NoReturn, Iterator[SplitsResponse]]:
        if limit < 1 or limit > 50:
            raise ValueError("Limit should be greater than or equal to 1 and less than or equal to 50")

        if offset < 0:
            raise ValueError("Offset should be greater than or equal to 0")

        split_definitions = self.__list_split_definitions_in_environment_chunk(wsid, environment_name,
                                                                               offset, limit, headers)
        if not split_definitions:
            log.error(f"Couldn't get split definitions list from '{environment_name}' environment")
            yield split_definitions
            return
        else:
            yield split_definitions

        split_definitions_payload = split_definitions.json()
        if split_definitions_payload['totalCount'] > split_definitions_payload['limit']:
            while split_definitions_payload['offset'] < split_definitions_payload['totalCount']:
                offset += limit
                split_definitions = self.__list_split_definitions_in_environment_chunk(wsid, environment_name,
                                                                                       offset, limit, headers)
                if split_definitions is None:
                    log.error(f"Couldn't get split definitions list from '{environment_name}' environment")
                    yield split_definitions
                    return
                else:
                    yield split_definitions
                split_definitions_payload = split_definitions.json()

    def kill_split_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            comment: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Killing split '{split_name}' in '{environment_id_or_name}' environment")
        put_resp = self.__session.put(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_id_or_name}/kill',
            headers=self.__method_scope_headers_update(headers or {}),
            json={"comment": f"{comment}"} if comment else None
        )

        return SplitsResponse(put_resp)

    def restore_split_in_environment(
            self,
            split_name: str,
            wsid: str,
            environment_id_or_name: str,
            comment: Optional[str] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> SplitsResponse:
        log.info(f"Restoring split '{split_name}' in '{environment_id_or_name}' environment")
        put_resp = self.__session.put(
            f'{self.__hostname}/ws/{wsid}/{split_name}/environments/{environment_id_or_name}/restore',
            headers=self.__method_scope_headers_update(headers or {}),
            json={"comment": f"{comment}"} if comment else None
        )

        return SplitsResponse(put_resp)
