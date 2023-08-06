[![codecov](https://codecov.io/gl/hashmapinc:ctso:utilities/logitol/branch/%5Cx6d6173746572/graph/badge.svg?token=759MGZCR4Z)](https://codecov.io/gl/hashmapinc:ctso:utilities/logitol)

# logitol

logitol is a small library aimed to encapsulate various different logging approaches into a single place. And to be loaded/instantiated through a common interface.

## Concept
Logging is a rather universal need across all applications. However, there are times where the builtin python loggers are sufficient, and those where they are 
not. And so, in many cases, it is desirable to encapsulate in such a way that you can interchange loggers as needed - and to include all 'loggers' in a single 
library for consistency. 

## Design

There is a single entry point: *get_logger(logger_type, \*\*kwargs)*

## Examples

```python
from logitol import get_logger

logger = get_logger()
```
