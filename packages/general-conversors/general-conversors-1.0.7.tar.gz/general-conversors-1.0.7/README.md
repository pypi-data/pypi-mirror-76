# Multi-purposes conversors for Python
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://gitlab.com/goldenm-software/open-source-libraries/general-conversors/blob/master/LICENSE)
[![pypi version](https://badge.fury.io/py/general-conversors.svg)](https://pypi.org/project/general-conversors/)


## Installation
Use the package manager [pip](https://pypi.org/) to install general-conversors.

```bash
pip3 install general-conversors
```

## Usage
To 1-Level dictionary
```python
from conversor.dict import ToOneLevel

source = {
  'error': False,
  'result': {
    'executed': True,
    'payload': 'Hello world',
    'code': 200,
    'source_code_url': 'http://google.com'
  }
}

## replace_underscore as True
conversor = ToOneLevel(source=source, replace_underscore=True)
result = conversor.convert()
print('Result replacing underscore:', result)
# Result replacing underscore: {'error': False, 'result.executed': True, 'result.payload': 'Hello world', 'result.code': 200, 'result.source.code.url': 'http://google.com'}

## replace_underscore as False (Default)
conversor = ToOneLevel(source=source)
result = conversor.convert()
print('Result:', result)
# Result: {'error': False, 'result.executed': True, 'result.payload': 'Hello world', 'result.code': 200, 'result.source_code_url': 'http://google.com'}

```
To N-level level dictionary
```python
from conversor.dict import ToMultiLevel

source = {
  'error': False,
  'result.executed': True,
  'result.payload': 'Hello world',
  'result.code': 200
}

conversor = ToMultiLevel(source=source)
result = conversor.convert()
print('Result:', result)
# Result: {'error': False, 'result': {'executed': True, 'payload': 'Hello world', 'code': 200}}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)