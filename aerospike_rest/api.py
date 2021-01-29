import requests

from aerospike_rest import NAME, get_version
from aerospike_rest.exceptions import AerospikeRestApiError

import logging
logger = logging.getLogger(__name__)


class AerospikeRestApi(object):
    def __init__(self, base_url, authorization=None, user_agent=None,
                 connect_timeout=2, client_compression=True,
                 http_compression=True):
        """
        Requests wrapper to make API calls to Aerospike REST Client.

        Args:
            base_url            - Absolute URL to Aerospike REST Client
            authorization       - Aerospike user:password
            user_agent          - User-agent string included in requests
            connect_timeout     - Connect timeout for all requests in seconds
            client_compression  - Enable compression between REST and Aerospike
            http_compression    - Enable compression between this and REST
        """
        self.base_url = base_url.rstrip("/")
        if base_url[0:4] == "http":
            self.base_url = self.base_url
        else:
            self.base_url = "https://" + self.base_url

        self.authorization = authorization
        self.client_compression = client_compression
        self.http_compression = http_compression
        self.connect_timeout = connect_timeout

        if not user_agent:
            self.user_agent = "{}/{}".format(NAME, get_version())
        else:
            self.user_agent = user_agent

        # use keep-alive
        self.session = requests.Session()


    def request(self, request_func, path, body=None, params=None, 
                 headers=None, timeout=30):
        """
        Send HTTP request to Aerospike REST client endpoint.
        """
        all_params = {
            'compress': self.client_compression
        }

        if params:
            all_params.update(params)

        all_headers = {
            'User-Agent': self.user_agent
        }

        if self.http_compression:
            all_headers['Accept-Encoding'] = 'gzip'
        
        if self.authorization:
            all_headers['Authorization'] = self.authorization

        if headers:
            all_headers.update(headers)

        url = "{}/{}".format(self.base_url, path.lstrip("/"))
        response = request_func(url, params=all_params, json=body,
                                headers=all_headers,
                                timeout=(self.connect_timeout, timeout))

        logger.debug("--- [REQUEST] ----------------------------------")
        for k, v in response.request.headers.items():
            logger.debug("{:24}: {}".format(k, v))
        logger.debug(response.request.body)

        logger.debug("--- [RESPONSE] ---------------------------------")
        for k, v in response.headers.items():
            logger.debug("{:24}: {}".format(k, v))
        content = response.content.decode("utf-8")
        logger.debug("Body:\n{}".format(content or "<EMPTY BODY>"))

        try:
            json = response.json()
            if response.status_code in (404, 403, 409):
                raise AerospikeRestApiError(json, response.status_code)
            return json
        except ValueError:
            # The response was not valid JSON (empty body, 5xx errors, etc.)
            response.raise_for_status()


    def get(self, path, body=None, params=None, headers=None, timeout=30):
        """
        Return UTF-8 response body from HTTP GET request to Aerospike REST
        Client endpoint.

        Args:
            path    - API path relative to base_url
            body    - HTTP request body (sent as application/json)
            params  - Dictionary of request query string parameters
            timeout - Read timeout in seconds

        Raises:
            AerospikeRestClientError
        """
        return self.request(self.session.get, path, body, params, headers,
                            timeout)


    def post(self, path, body=None, params=None, headers=None, timeout=30):
        """
        Return UTF-8 response body from HTTP POST request to Aerospike REST
        Client endpoint.

        Args:
            path    - API path relative to base_url
            body    - HTTP request body (sent as application/json)
            params  - Dictionary of request query string parameters
            timeout - Read timeout in seconds

        Raises:
            AerospikeRestClientError
        """
        return self.request(self.session.post, path, body, params, headers,
                            timeout)


    def put(self, path, body=None, params=None, headers=None, timeout=30):
        """
        Return UTF-8 response body from HTTP PUT request to Aerospike REST
        Client endpoint.

        Args:
            path    - API path relative to base_url
            body    - HTTP request body (sent as application/json)
            params  - Dictionary of request query string parameters
            timeout - Read timeout in seconds

        Raises:
            AerospikeRestClientError
        """
        return self.request(self.session.put, path, body, params, headers,
                            timeout)


    def delete(self, path, body=None, params=None, headers=None, timeout=30):
        """
        Return UTF-8 response body from HTTP DELETE request to Aerospike REST
        Client endpoint.

        Args:
            path    - API path relative to base_url
            body    - HTTP request body (sent as application/json)
            params  - Dictionary of request query string parameters
            timeout - Read timeout in seconds

        Raises:
            AerospikeRestClientError
        """
        return self.request(self.session.delete, path, body, params, headers,
                            timeout)


    def patch(self, path, body=None, params=None, headers=None, timeout=30):
        """
        Return UTF-8 response body from HTTP PATCH request to Aerospike REST
        Client endpoint.

        Args:
            path    - API path relative to base_url
            body    - HTTP request body (sent as application/json)
            params  - Dictionary of request query string parameters
            timeout - Read timeout in seconds

        Raises:
            AerospikeRestClientError
        """
        return self.request(self.session.patch, path, body, params, headers,
                            timeout)
