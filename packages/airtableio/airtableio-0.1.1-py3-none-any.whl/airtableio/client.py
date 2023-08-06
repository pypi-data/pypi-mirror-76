import asyncio
import contextlib
import io
from contextvars import ContextVar
from typing import Dict, List, Optional, Text, Type, Union

import aiohttp
from aiohttp.helpers import sentinel

from . import api


class Client(object):
    """
    Class represents client.
    """

    _ctx_timeout = ContextVar("AirtableRequestTimeout")
    _ctx_token = ContextVar("AirtableToken")
    _ctx_app_id = ContextVar("AirtableAppId")

    def __init__(
        self,
        token: Text,
        app_id: Text,
        loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
        connections_limit: Optional[int] = None,
        timeout: Optional[Union[int, float, aiohttp.ClientTimeout]] = None,
    ):
        self._token = None
        self.__token = token

        self._app_id = None
        self.__app_id = app_id

        # Asyncio loop instance
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        # aiohttp main session
        self._session: Optional[aiohttp.ClientSession] = None
        self._connector_class: Type[aiohttp.TCPConnector] = aiohttp.TCPConnector
        self._connector_init = dict(limit=connections_limit, loop=self.loop)

        self._timeout = None
        self.timeout = timeout

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init), loop=self.loop
        )

    @property
    def session(self) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    @staticmethod
    def _prepare_timeout(
        value: Optional[Union[int, str, aiohttp.ClientTimeout]]
    ) -> Optional[aiohttp.ClientTimeout]:
        if value is None or isinstance(value, aiohttp.ClientTimeout):
            return value
        return aiohttp.ClientTimeout(total=value)

    @property
    def timeout(self):
        timeout = self._ctx_timeout.get(self._timeout)
        if timeout is None:
            return sentinel
        return timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = self._prepare_timeout(value)

    @timeout.deleter
    def timeout(self):
        self.timeout = None

    @contextlib.contextmanager
    def request_timeout(self, timeout: Union[int, float, aiohttp.ClientTimeout]):
        """
        Context manager implements opportunity to change request timeout in current context
        :param timeout: Request timeout
        :type timeout: :obj:`typing.Optional[typing.Union[base.Integer, base.Float, aiohttp.ClientTimeout]]`
        :return:
        """
        timeout = self._prepare_timeout(timeout)
        token = self._ctx_timeout.set(timeout)
        try:
            yield
        finally:
            self._ctx_timeout.reset(token)

    @property
    def __token(self):
        return self._ctx_token.get(self._token)

    @__token.setter
    def __token(self, value):
        self._token = value

    @contextlib.contextmanager
    def with_token(self, token: Text):
        token = self._ctx_token.set(token)
        try:
            yield
        finally:
            self._ctx_token.reset(token)

    @property
    def __app_id(self):
        return self._ctx_app_id.get(self._app_id)

    @__app_id.setter
    def __app_id(self, value):
        self._app_id = value

    @contextlib.contextmanager
    def with_app_id(self, app_id: Text):
        app_id = self._ctx_app_id.set(app_id)
        try:
            yield
        finally:
            self._ctx_app_id.reset(app_id)

    async def close(self):
        """
        Close all client sessions
        """
        await self.session.close()

    async def request(
        self,
        method: Text,
        table_name: Text,
        data: Optional[Union[Dict, List]] = None,
        record_id: Optional[Text] = None,
        **kwargs
    ) -> Union[List, Dict, bool]:
        """
        Make a request to Airtable API
        https://airtable.com/api
        :param method: API method
        :type method: :obj: Text
        :param data: request parameters
        :type data: :obj:`dict`
        :return: result
        :rtype: Union[List, Dict]
        :raise: :obj:``
        """
        return await api.make_request(
            self.session,
            self.__token,
            method,
            self.__app_id,
            table_name,
            data,
            record_id,
            timeout=self.timeout,
            **kwargs
        )
