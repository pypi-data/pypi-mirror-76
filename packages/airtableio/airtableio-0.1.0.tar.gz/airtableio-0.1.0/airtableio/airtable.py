"""
This module contains application layer.

!!!This module contains methods developed by airtable-python-wrapper!!!
Link — https://github.com/gtalarico/airtable-python-wrapper/blob/fa1fbf8c91649e47ef13dd663856a41a4601c296/airtable/airtable.py#L164

Copyright (c) 2017 Gui Talarico

"""

import asyncio
import datetime
from typing import Dict, Iterable, List, Text, Any

from . import Client, api
from .helpers import AirtableParams


class Airtable(Client):
    """
    Main class for interacting with Airtable API.

    :param Client: :class: Client
    """

    API_LIMIT = 1.0 / 5  # 5 per second
    MAX_RECORDS_PER_REQUEST = 10

    # this developed by airtable-python-wrapper
    def _chunk(self, iterable: Iterable, chunk_size: int) -> Iterable:
        """"Break iterable into chunks."""
        for i in range(0, len(iterable), chunk_size):
            yield iterable[i : i + chunk_size]

    # this developed by airtable-python-wrapper
    def _build_batch_record_objects(self, records: Dict) -> Dict:
        return {"records": [record for record in records]}

    async def get_records(self, table_name: Text, **kwargs) -> Dict:
        """
        Method to List Table records.

        :param table_name: Text
        :return: Records 
        :rtype: Dict
        """
        result = await self.request(
            api.Methods.GET_RECORDS, table_name=table_name, **kwargs
        )
        return result

    async def get_record_by_field(
        self, table_name: Text, field_name: Text, field_value: Any, **kwargs
    ) -> Dict:
        from_name_and_value = AirtableParams.FormulaParam.from_name_and_value
        formula = from_name_and_value(field_name, field_value)
        param = {"filterByFormula": formula}
        result = await self.get_records(table_name, params=param)
        if result:
            return result
        else:
            return {}

    async def get_record(self, table_name: Text, record_id: Text) -> Dict:
        """
        Method to Retrieve a Table record.

        :param table_name: Text
        :param record_id: Text
        :return: Record
        :rtype: Dict
        """
        result = await self.request(
            api.Methods.GET_RECORD, table_name=table_name, record_id=record_id
        )
        return result

    async def _bulk_create_records(self, table_name: Text, data: Dict) -> Dict:
        # TODO: could be refactored for every method with records limitation
        inserted_records = []
        for chunk in self._chunk(
            data["records"], self.MAX_RECORDS_PER_REQUEST
        ):  # 10 is a max records per requests
            new_records = self._build_batch_record_objects(chunk)
            response = await self.request(
                api.Methods.CREATE_RECORDS, table_name=table_name, data=new_records
            )
            inserted_records += response["records"]
            await asyncio.sleep(self.API_LIMIT)
        return inserted_records

    async def create_records(self, table_name: Text, data: Dict) -> Dict:
        """
        Method to Create Teable records.

        :param table_name: Text
        :param data: Dict
        :return: Inserted records
        :rtype: Dict
        """

        if len(data["records"]) < 10:  # Airtable accepts only 10 objects per request
            result = await self.request(
                api.Methods.CREATE_RECORDS, table_name=table_name, data=data
            )
            return result
        else:
            result = await self._bulk_create_records(table_name, data)
            return result

    async def update_records(self, table_name: Text, data: Dict) -> Dict:
        """
        Method to Update Table records.

        :param table_name: Text
        :param data: Dict
        :return: Updated records
        :rtype: Dict
        """
        if len(data) < 10:  # Airtable accepts only 10 objects per request
            result = await self.request(
                api.Methods.UPDATE_RECORDS, table_name=table_name, data=data
            )
            return result
        else:
            # slice the request
            return

    async def delete_records(self, table_name: Text, data: Dict) -> Dict:
        """
        Method to Delete Table records.

        :param table_name: Text
        :param record_id: Text
        :return: Deleted records
        :rtype: Dict
        """
        if len(data) < 10:  # Airtable accepts only 10 objects per request
            result = await self.request(
                api.Methods.DELETE_RECORDS, table_name=table_name, params=data
            )
            return result
        else:
            # slice the request
            return
