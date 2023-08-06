# Constants and Utils

Package with constants and generic utilities

[![pipeline status](https://gitlab.com/terminus-zinobe/constants-and-utils/badges/master/pipeline.svg)](https://gitlab.com/terminus-zinobe/constants-and-utils/-/commits/master) [![coverage report](https://gitlab.com/terminus-zinobe/constants-and-utils/badges/master/coverage.svg)](https://gitlab.com/terminus-zinobe/constants-and-utils/-/commits/master)


## Package installation
- Installation standard
    ```shell
    $ pip3 install constants-and-utils
    ```

- Install with mongoengine utils
    ```shell
    $ pip3 install constants-and-utils[mongoengine]
    ```

## Docs

- [Constants and utils documentation](https://constants-and-utils-docs.readthedocs.io/en/latest/index.html)

Examples:

`recursive_get` this is a helper, apply a get recursive to the dictionary.

```python
>>> from constants_and_utils.utils.helpers import recursive_get

>>> recursive_get({'NUMBER': {'ONE': 1 }}, 'NUMBER.ONE')
1
```


`HttpCode` this is a class enum, Http code constants.

```python
>>> from constants_and_utils.constants.enums import HttpCode

>>> HttpCode.OK.value
200
```
[More](https://constants-and-utils-docs.readthedocs.io/en/latest/index.html)
