import logging
import os
from http import HTTPStatus

import aiohttp

from .exceptions import AirtableAPIError

LOG = logging.getLogger("airtable")
logging.basicConfig(level="DEBUG")

API_URL = "https://api.airtable.com/v0/{app_id}/{table_name}"


async def make_request(
    session, token, method, app_id, table_name, data=None, record_id=None, **kwargs
):
    LOG.debug('Make request: "%s" with data: "%r', method, data)

    url = Methods.api_url(app_id=app_id, table_name=table_name, record_id=record_id)
    req = data
    headers = {"Authorization": "Bearer {}".format(token)}

    if method == "post":
        try:
            async with session.post(
                url, json=req, headers=headers, **kwargs
            ) as response:
                result = await response.json()
                return result
        except aiohttp.ClientError as e:
            raise AirtableAPIError(
                f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
            )
    elif method == "get":
        try:
            async with session.get(url, headers=headers, **kwargs) as response:
                result = await response.json()
                LOG.debug("Got result from get query: {}".format(result))
                return result
        except aiohttp.ClientError as e:
            raise AirtableAPIError(
                f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
            )
    elif method == "put":
        try:
            async with session.put(
                url, data=req, headers=headers, **kwargs
            ) as response:
                result = await response.json()
                return result
        except aiohttp.ClientError as e:
            raise AirtableAPIError(
                f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
            )
    elif method == "patch":
        try:
            async with session.patch(
                url, data=req, headers=headers, **kwargs
            ) as response:
                result = await response.json()
                return result
        except aiohttp.ClientError as e:
            raise AirtableAPIError(
                f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
            )
    elif method == "delete":
        try:
            async with session.delete(url, headers=headers, **kwargs) as response:
                result = await response.json()
                return result
        except aiohttp.ClientError as e:
            raise AirtableAPIError(
                f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
            )


def compose_data(params=None):
    """
    Prepare request data
    :param params:
    :return:
    """
    data = aiohttp.formdata.FormData(quote_fields=False)

    if params:
        for key, value in params.items():
            data.add_field(key, str(value))

    return data


class Methods:

    GET_RECORDS = "get"
    GET_RECORD = "get"
    CREATE_RECORDS = "post"
    UPDATE_RECORDS = "patch"
    DELETE_RECORDS = "delete"

    @staticmethod
    def api_url(app_id, table_name, record_id=None):
        """
        Generate API URL with included token and method name
        :param app_id:
        :param table_name:
        :return:
        """
        if record_id:
            return (
                API_URL.format(app_id=app_id, table_name=table_name) + "/" + record_id
            )
        else:
            return API_URL.format(app_id=app_id, table_name=table_name)
