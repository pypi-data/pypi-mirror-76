# hopy
A high level language for predicate evaluation on JSON using JsonPath expressions

## Getting started

### Prerequisites
- python3.7+

### Installation
- Install the package using pip.
    ```bash
    pip install hopy[jsonpath_ng]
    ```

### Usage
```python
from hopy.evaluator import HopyEvaluator

rule_payload = {
    "str": "Hello World!",
    "num": 1337,
    "float": 13.37,
    "nested": {
        "str": "Hello again!"
    }
}
rule = '`$.str` == "Hello World!" && (`$.num` == 1337 || `$.float` < 13) && f.in(f.lower(`$.nested.str`), "hello")'

rule_evaluator = HopyEvaluator(rule)
rule_evaluator.evaluate(rule_payload) # True
```

## License
This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements
- Inspired from [santanusinha/hope](https://github.com/santanusinha/hope)
- Default JsonPath implementation [jsonpath-ng](https://pypi.org/project/jsonpath-ng/)
