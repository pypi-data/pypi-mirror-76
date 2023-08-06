"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from globomap_api_client.base import Base


class Edge(Base):

    def post(self, document):
        return self.make_request(method='POST', uri='edges', data=document)

    def search(self, query=None, per_page=10, page=1):
        uri = 'edges'
        query = self.encoding_params(query)
        params = {
            'query': query,
            'per_page': per_page,
            'page': page
        }
        return self.make_request(method='GET', uri=uri, params=params)

    def list(self, per_page=10, page=1):
        uri = 'edges'
        params = {
            'per_page': per_page,
            'page': page
        }
        return self.make_request(method='GET', uri=uri, params=params)
