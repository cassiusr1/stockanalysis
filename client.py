from polygon import RESTClient
import test
import json
from typing import cast
from urllib3 import HTTPResponse



client = RESTClient(test.api_key)

aggs = cast(
    HTTPResponse,
    client.get_aggs(
        'AAPL',
        1,
        'day',
        '2025-01-01',
        '2025-01-22',
        raw=True

    )
)

data = json.loads(aggs.data)
print(data)

