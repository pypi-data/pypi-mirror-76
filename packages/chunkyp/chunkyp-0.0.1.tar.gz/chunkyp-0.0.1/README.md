# chunkyp

A small and concise data preprocessing library inspired by common NLP preprocessing workflows. 

Supports [ray](https://github.com/ray-project/ray).

## Installation
chunkyp is available on PyPi.
```bash
pip install chunkyp
```

For the dev version you can run the following.
```bash
git clone https://github.com/neophocion/chunkyp
cd chunkyp
pip install -e .
```

## Usage

The simplest way to get started is to look at the Jupyter notebooks in [`notebooks/`](https://github.com/neophocion/chunkyp/tree/master/notebooks)

A small example:

```python
from chunkyp import 

res = pipe(
    records, # a list, or iterator across, dicts
    p('field', lambda x: x.lower()),
    p('field', lambda x: x.upper(), 'new_field'),
    p(['field1', 'field2'], lambda x,y: len(x.split()) == y, 'new_field2'),
)

res = list(res)
res
```
