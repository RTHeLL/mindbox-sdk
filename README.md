# Mindbox Python API

Wrapper for working with Mindbox service API

[![N|Solid](https://img.shields.io/pypi/pyversions/mindbox-sdk.svg)](https://pypi.python.org/pypi/mindbox-sdk)

### Installation
You can install or upgrade package with:
```
$ pip install mindbox-sdk --upgrade
```
Or you can install from source with:
```
$ git clone https://github.com/RTHeLL/mindbox-sdk
$ cd mindbox-sdk
$ python setup.py install
```
...or install from source buth with pip
```
$ pip install git+https://github.com/RTHeLL/mindbox-sdk
```
### Example

```python
from mindbox.client import MindboxClient


def main():
    mindbox_client = MindboxClient(endpoint_id="YOUR_ENDPOINT_ID", secret_key="YOUR_SECRET_KEY", type_="async")
    client = mindbox_client.operations.get_client(
        "Getclient",
        **{
            "customer": {
                "mobilePhone": "+79374134388"
            }
        }
    )

    print(
        f'Client: {client}'
    )


main()
```


## Bugs

If you have any problems, please create Issues [here](https://github.com/RTHeLL/mindbox-sdk/issues)  
