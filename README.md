Python interface to the Aerospike REST Client.

A convenience wrapper around [requests](https://requests.readthedocs.io/en/master/) for using the [Aerospike REST Client](https://www.aerospike.com/docs/client/rest/index.html) in Python.

**Simple Example**

```python
api = AerospikeRestApi('http://localhost:8080/v1')
bins = {'mybin': "Hello World!"}
api.post('/kvs/mynamespace/myset/mykey', bins)
```

**Exceptions**

```python
from aerospike_rest.api import AerospikeRestApi

api = AerospikeRestApi('http://localhost:8080/v1')
bins = {'mybin': "Hello World!"}
params = {
    'recordExistsAction': "CREATE_ONLY"
}
try:
    api.post('/kvs/mynamespace/myset/mykey', bins, params)
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
