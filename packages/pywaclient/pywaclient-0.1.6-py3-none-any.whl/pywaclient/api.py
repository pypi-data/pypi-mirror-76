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

from pywaclient.endpoints.article import Article
from pywaclient.endpoints.block import Block
from pywaclient.endpoints.image import Image
from pywaclient.endpoints.manuscript import Manuscript
from pywaclient.endpoints.user import User
from pywaclient.endpoints.world import World


class AragornApiClient:

    def __init__(self,
                 name: str,
                 url: str,
                 version: str,
                 application_key: str,
                 authentication_token: str,
                 ):
        self.headers = {
            'x-auth-token': authentication_token,
            'x-application-key': application_key,
            'Accept': 'application/json',
            'User-Agent': f'{name} ({url}, {version})'
        }
        self.base_url = 'https://www.worldanvil.com/api/aragorn/'
        self.block = Block(self)
        self.article = Article(self)
        self.image = Image(self)
        self.manuscript = Manuscript(self)
        self.user = User(self)
        self.world = World(self)
