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
import time

from requests import Session

from globomap_api_client import exceptions
from globomap_api_client.settings import SSL_VERIFY

logger = logging.getLogger(__name__)


class Base(object):

    def __init__(self, auth, retries=10):
        self.auth = auth
        self.retries = retries
        self.session = Session()

    def _get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token token={}'.format(self.auth.token)
        }
        return headers

    def make_request(self, method, uri, params=None, data=None, retries=0):
        if uri[-1] != '/':
            uri += '/'
        request_url = '{}/v2/{}'.format(self.auth.api_url, uri)

        if type(data) is dict or type(data) is list:
            data = json.dumps(data)
        headers = self._get_headers()
        try:
            if method in ('GET', 'DELETE'):
                if method == 'GET':
                    headers.pop('Content-Type')
                response = self.session.request(
                    method,
                    request_url,
                    params=params,
                    headers=headers,
                    verify=SSL_VERIFY
                )
            else:
                response = self.session.request(
                    method,
                    request_url,
                    data=data,
                    headers=headers,
                    verify=SSL_VERIFY
                )
            logger.info('REQUEST: %s %s', method, request_url)
        except Exception:
            logger.exception('Error in request')
            raise exceptions.ApiError('Error in request')

        else:
            try:
                content = response.json()
            except json.JSONDecodeError:
                content = response.content

            status_code = response.status_code

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('RESPONSE: %s %s %s %s',
                             method, request_url, content, status_code)
            else:
                logger.info('RESPONSE: %s %s %s', method,
                            request_url, status_code)

            if status_code in (502, 503) and retries < self.retries:
                retries += 1
                self.make_request(method, uri, params, data, retries)
            elif status_code == 500:
                retries_error = self.retries - 6
                if retries < retries_error:
                    logger.warning('Retry send %s %s %s %s',
                                    method, request_url, params, data)
                    retries += 1
                    time.sleep(retries * 5)
                    self.make_request(method, uri, params, data, retries)

            return self._parser_response(content, status_code)

    def _parser_response(self, content, status_code):
        if status_code == 200:
            return content
        elif status_code == 400:
            raise exceptions.ValidationError(content, status_code)
        elif status_code == 401:
            raise exceptions.Unauthorized(content, status_code)
        elif status_code == 403:
            raise exceptions.Forbidden(content, status_code)
        elif status_code == 404:
            raise exceptions.NotFound(content, status_code)
        elif status_code == 409:
            raise exceptions.DocumentAlreadyExists(content, status_code)
        else:
            raise exceptions.ApiError(content, status_code)

    def encoding_params(self, params):
        params = json.dumps(params)
        return params
