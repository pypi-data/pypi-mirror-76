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
import json
import logging

from requests import Session

from globomap_api_client import exceptions
from globomap_api_client.settings import SSL_VERIFY


class Auth(object):

    logger = logging.getLogger(__name__)

    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.session = Session()
        self.generate_token()

    def generate_token(self):
        response = self._make_request()
        self.auth = response
        self.token = response['token']

    def _get_headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def _make_request(self):
        try:
            url = '{}/v2/auth/'.format(self.api_url)
            data = {
                'username': self.username,
                'password': self.password
            }
            response = self.session.request(
                'POST',
                url,
                data=json.dumps(data),
                headers=self._get_headers(),
                verify=SSL_VERIFY
            )

        except Exception:
            self.logger.exception('Error in request')
            raise exceptions.ApiError('Error in request')

        else:
            return self._parser_response(response)

    def _parser_response(self, response):
        content = response.json()
        status_code = response.status_code

        if status_code == 200:
            return content
        elif status_code == 400:
            raise exceptions.ValidationError(content, status_code)
        elif status_code == 401:
            raise exceptions.Unauthorized(content, status_code)
        else:
            raise exceptions.ApiError(content, status_code)
