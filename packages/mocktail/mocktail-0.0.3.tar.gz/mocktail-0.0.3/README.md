Mocktail
========

The non-alcoholic, Mockito-inspired utility for `unittest.mock`!

[![Build Status](https://travis-ci.org/koirikivi/mocktail.svg?branch=master)](https://travis-ci.org/koirikivi/mocktail)

This package provides dead-simple utilities for setting return values for mocks
with a Mockito-inspired syntax:

```python
from unittest.mock import MagicMock
from mocktail import when

my_mock = MagicMock()
when(my_mock).some_method('foo').then_return('bar')

my_mock.some_method('foo')  # 'bar'
```

Unlike other solutions (like [mockito-python](https://github.com/kaste/mockito-python)),
it deliberately only works with mocks created using `unittest.mock`. To set the return
values of arbitrary objects, combine with `unittest.mock.patch`.

Installation
------------

`pip install mocktail`

Buyer beware!
-------------

This package -- though very minimal -- is in early alpha stage. Use with your own
risk!

Contributing
------------

Pull requests and bug reports are gladly accepted in this Github repository.


License
-------

MIT

TODO
----

- (More) matchers
- Matcher for "rest of args / kwargs"
- `verify` syntax
- Docs
