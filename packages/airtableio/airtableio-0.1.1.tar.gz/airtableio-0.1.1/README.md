**Async API wrapper for Airtable.**
=====================
Powered by aiohttp.
https://airtable.com/

**Simple Usage**

```python 

from airtableio import Airtable
import asyncio

TOKEN = ""
APP_ID = ""

my_airtable = Airtable(TOKEN, APP_ID)


async def call():
    result = await my_airtable.get_records("Table")
    print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(call())

    loop.run_forever()
```
