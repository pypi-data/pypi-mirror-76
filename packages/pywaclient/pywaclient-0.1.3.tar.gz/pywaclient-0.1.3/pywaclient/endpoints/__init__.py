#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import requests
import logging
import json
from typing import Dict, Any, Iterable


class Endpoint:

    def __init__(self, client: 'AragornApiClient'):
        self.client = client

    def _request(self, path: str, **kwargs) -> Dict[str, Any]:
        logging.debug(f'Requesting {self.client.base_url + path} with headers {self.client.headers} and {kwargs}')
        response = requests.get(self.client.base_url + path, params=kwargs, headers=self.client.headers)
        if response.ok:
            return json.loads(response.text)
        else:
            return {
                'status': response.status_code,
                'error': response.reason
            }

    def _scroll_collection(self, path: str, collection_tag: str, **kwargs) -> Iterable[Dict[str, Any]]:
        limit = 50
        offset = 0
        items = self._request(path, **kwargs)[collection_tag]
        while len(items) > 0:
            for item in items:
                yield item
            offset += 1
            kwargs['offset'] = offset * limit
            items = self._request(path, **kwargs)[collection_tag]
