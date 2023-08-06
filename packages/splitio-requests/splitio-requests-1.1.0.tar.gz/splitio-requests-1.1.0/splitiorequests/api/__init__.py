# -*- coding: utf-8 -*-


from abc import ABC
from typing import Optional, Dict, Tuple, NoReturn, Union
from requests import Session
from urllib3.util.retry import Retry

from ..common.http_adapter import TimeoutHTTPAdapter
from .splits import SplitsRequests
from .environments import EnvironmentsRequests
from .workspaces import WorkspacesRequests
from .traffic_types import TrafficTypesRequests
from .tags import TagsRequests


class APIRequestsBase(ABC):
    def __init__(
            self,
            token: str,
            hostname: Optional[str] = None
    ) -> None:
        self._hostname = hostname or 'https://api.split.io/internal/api/v2'
        self._headers = {'Authorization': f"Bearer {token}"}

    def _super_session(
            self,
            retries: int,
            backoff_factor: float,
            status_forcelist: Tuple[int, ...],
            session: Optional[Session]
    ) -> Union[NoReturn, Session]:
        raise NotImplementedError


class AdminAPI(APIRequestsBase):
    def __init__(
            self,
            token: str,
            headers: Optional[Dict[str, str]] = None,
            hostname: Optional[str] = None,
            retries: int = 10,
            backoff_factor: float = 0.3,
            status_forcelist=(429, 500, 502, 503, 504),
            session: Optional[Session] = None,
    ) -> None:
        super().__init__(token, hostname)
        self._headers.update(headers or {})
        self.__session = self._super_session(retries, backoff_factor, status_forcelist, session)
        self.__splits = SplitsRequests(self._headers, self._hostname, self.__session)
        self.__environments = EnvironmentsRequests(self._headers, self._hostname, self.__session)
        self.__workspaces = WorkspacesRequests(self._headers, self._hostname, self.__session)
        self.__traffic_types = TrafficTypesRequests(self._headers, self._hostname, self.__session)
        self.__tags = TagsRequests(self._headers, self._hostname, self.__session)

    def _super_session(
            self,
            retries: int,
            backoff_factor: float,
            status_forcelist: Tuple[int, ...],
            session: Optional[Session]
    ) -> Session:
        session = session or Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH", "POST"]
        )
        adapter = TimeoutHTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        return session

    @property
    def splits(self):
        return self.__splits

    @property
    def environments(self):
        return self.__environments

    @property
    def workspaces(self):
        return self.__workspaces

    @property
    def traffic_types(self):
        return self.__traffic_types

    @property
    def tags(self):
        return self.__tags
