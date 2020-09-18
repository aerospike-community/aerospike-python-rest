from unittest import TestCase
from unittest.mock import MagicMock, patch

from copy import deepcopy
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError

from aerospike_rest import NAME, get_version
from aerospike_rest.api import AerospikeRestApi
from aerospike_rest.exceptions import AerospikeRestApiError


class TestAerospikeRestApi(TestCase):
    wrapper_methods = (
        ('requests.Session.get', 'get'),
        ('requests.Session.post', 'post'),
        ('requests.Session.put', 'put'),
        ('requests.Session.patch', 'patch'),
        ('requests.Session.delete', 'delete')
    )

    default_headers = {
        'User-Agent': "{}/{}".format(NAME, get_version()), 
        'Accept-Encoding': 'gzip'
    }

    default_params = {
        'compress': True
    }

    default_timeout = 30

    def test_init(self):
        """
        AerospikeRestApi initializes class properties from initializer.
        """
        kwargs = {
            'base_url': 'http://foo',
            'authorization': 'b',
            'user_agent': 'c',
            'connect_timeout': 'd',
            'client_compression': 'e',
            'http_compression': 'f',
        }

        api = AerospikeRestApi(**kwargs)
        for k,v in kwargs.items():
            self.assertEqual(getattr(api, k), v)


    def test_url_sanitization(self):
        """
        AerospikeRestApi enforces scheme and strips trailing slash.
        """
        expected_url = 'http://foo'

        api = AerospikeRestApi('http://foo/')
        self.assertEqual(api.base_url, expected_url)

        api = AerospikeRestApi('foo/')
        self.assertEqual(api.base_url, expected_url)


    def test_method_wrappers(self):
        """
        AerospikeRestApi HTTP method wrappers map to requests.session functions.
        """
        api = AerospikeRestApi('http://foo')
        
        for patch_method, api_method in self.wrapper_methods:
            with patch(patch_method) as mock:
                getattr(api, api_method)('/bar')
                mock.assert_called_once()

    def _mock_client_success_response(self):
        return {
            "inDoubt": False,
            "internalErrorCode": 0,
            "message": "success message"
        }

    def test_success_response(self):
        """
        AerospikeRestApi returns JSON on success.
        """
        for patch_method, api_method in self.wrapper_methods:
            with patch(patch_method) as mock:
                api = AerospikeRestApi('http://foo')
                obj = MagicMock()
                obj.status_code = 200
                obj.json = self._mock_client_success_response
                mock.return_value = obj
                json = getattr(api, api_method)("/bar")
                self.assertEqual(json, self._mock_client_success_response())


    def _mock_client_error_response(self):
        return {
            "inDoubt": True,
            "internalErrorCode": -1,
            "message": "error message"
        }

    def test_expected_status_exceptions(self):
        """
        AerospikeRestApi raises AerospikeRestApiError for expected HTTP status
        codes.
        """
        with patch('requests.Session.get') as mock:
            for status_code in (403, 404, 409):
                api = AerospikeRestApi('http://foo')
                obj = MagicMock()
                obj.status_code = status_code
                obj.json = self._mock_client_error_response
                mock.return_value = obj
                with self.assertRaises(AerospikeRestApiError) as cm:
                    api.get("/bar")
                self.assertEqual(cm.exception.status_code, status_code)


    def _mock_json_decode_error(self):
        raise JSONDecodeError('test message', 'doc', 1)

    def test_unexpected_status_exceptions(self):
        """
        AerospikeRestApi raises underlying exception for unexpected status
        codes.
        """
        with patch('requests.Session.get') as mock:
            for status_code in (410, 205, 500):
                api = AerospikeRestApi('http://foo')
                obj = MagicMock()
                obj.status_code = status_code
                obj.json = self._mock_json_decode_error
                mock.return_value = obj
                api.get("/bar")
                obj.raise_for_status.assert_called()


    def _success_called_with(self, api, headers=None, params=None, 
                             timeout=30):
        """
        Helper method to test successful requests get called a certain way
        """
        for patch_method, api_method in self.wrapper_methods:
            with patch(patch_method) as mock:
                obj = MagicMock()
                obj.status_code = 200
                obj.json = self._mock_client_success_response
                mock.return_value = obj

                getattr(api, api_method)("/bar", headers=headers, params=params,
                                         timeout=timeout)
                
                all_headers = deepcopy(self.default_headers)
                all_headers['User-Agent'] = api.user_agent
                if headers:
                    all_headers.update(headers)
                if not api.http_compression:
                    all_headers.pop('Accept-Encoding')
                if api.authorization:
                    all_headers['Authorization'] = api.authorization

                all_params = deepcopy(self.default_params)
                if params:
                    all_params.update(params)
                if not api.client_compression:
                    all_params['compress'] = False

                if not timeout:
                    timeout = self.default_timeout

                mock.assert_called_with("http://foo/bar", headers=all_headers, 
                                        params=all_params, json=None,
                                        timeout=(api.connect_timeout, timeout))


    def test_optional_headers(self):
        """
        AerospikeRestApi should override default headers with arg headers
        """
        api = AerospikeRestApi('http://foo')
        self._success_called_with(api, headers={"Foo": "Bar"})


    def test_optional_params(self):
        """
        AerospikeRestApi should override default params with arg params
        """
        api = AerospikeRestApi('http://foo')
        self._success_called_with(api, params={"Foo": "Bar"})


    def test_optional_timeout(self):
        """
        AerospikeRestApi should override default timeouts
        """
        api = AerospikeRestApi('http://foo')
        api.connect_timeout = 999
        self._success_called_with(api, timeout=999)


    def test_optional_compression(self):
        """
        AerospikeRestApi should allow override of default compression
        """
        api = AerospikeRestApi('http://foo')
        api.client_compression = False
        api.http_compression = False
        self._success_called_with(api)


    def test_optional_authorization(self):
        """
        AerospikeRestApi should allow optional authorization header
        """
        api = AerospikeRestApi('http://foo')
        api.authorization = 'Basic abcdefg='
        self._success_called_with(api)


    def test_optional_user_agent(self):
        """
        AerospikeRestApi should allow optional user-agent
        """
        api = AerospikeRestApi('http://foo')
        api.user_agent = 'bar'
        self._success_called_with(api)