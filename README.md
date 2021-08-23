Python interface to the Aerospike REST Client.

Provides a simple convenience wrapper around [requests](https://requests.readthedocs.io/en/master/) for using the [Aerospike REST Client](https://www.aerospike.com/docs/client/rest/index.html) in Python.

* Enable/disable compression
* Enable/disable authentication (via Authorization header)
* Override default user-agent header
* Override default connect and read timeouts
* Make use of keep-alive (for lifetime of object)
* Raise exceptions with Aerospike error codes


### Simple Example

``` python
from aerospike_rest.api import AerospikeRestApi

api = AerospikeRestApi('http://localhost:8080/v1')
bins = {'mybin': "Hello World!"}
api.post('/kvs/mynamespace/myset/mykey', bins)
```

### Advanced Example

``` python
from aerospike_rest.api import AerospikeRestApi
from aerospike_rest.exceptions import AerospikeRestApiError


api = AerospikeRestApi('http://localhost:8080/v1')
api.http_compression = False
api.client_compression = True
api.authorization = 'Authorization: Basic YWRtaW46YWRtaW4=' 

bins = {'mybin': "Hello World!"}
params = {
    'recordExistsAction': "CREATE_ONLY"
}
headers = {
    'X-Custom-Header': 'hello'
}

try:
    api.post('/kvs/mynamespace/myset/mykey', bins, params, headers, timeout=10)
except AerospikeRestApiError as err:
    if err.code == KEY_EXISTS_ERROR:
        pass
    else:
        raise err
```


Test
--------------------------------------------------------------------------------

Run unit tests from the root directory:

```
python -m unittest -v -b
```

View test coverage from root directory:

```
coverage run --source=aerospike_rest/ -m unittest -v -b && coverage report
```


Release
--------------------------------------------------------------------------------

1. Create version branch: `git checkout -b version/v1.0.0`)
2. Bump version in `aerospike_rest/__init__.py` and commit the change
3. Tag the commit: `git tag -a v1.0.0 -m 'Release v1.0.0`
4. Submit PR
