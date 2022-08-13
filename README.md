# What is this?
This is the api wrapper of Cloudflare Workers KV.  
This [repo](https://github.com/maguayo/python-workers-kv) wasn't compatible with bulk import, so I made my own wrapper instead.  
You can use this to store and retrieve data from your Cloudflare Workers KV much easier.

## Usage
```python
import workers_kv

# get these values from your Cloudflare account
# Create namespace
namespace = workers_kv.Namespace(account_id="WORKERS_KV_ACCOUNT",
                                 namespace_id="WORKERS_KV_NAMESPACE",
                                 api_key="TOKEN")

# List all keys
keys = namespace.list_keys()

# Get value with key
value = namespace.read("keyhere")

# Set value with key
# automatically use bulk import if you have more than 2 key-value pairs
namespace.write({"key1": "value1", "key2": "value2"})

# Delete single key
namespace.delete_one("key1")

# Delete multiple keys (bulk delete)
namespace.delete_many(["key1", "key2"])
```


## Installation
`pip install -U git+https://github.com/Alpaca131/workers-kv-py.git`