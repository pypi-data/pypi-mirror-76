# `lonny_common_sql`

A library for building inline SQL queries safely using python `callables`.

## Installation:

```bash
pip install lonny_common_sql
```

## Usage:

Usage is very straightforward. Please see example below:

```python
from lonny_common_sql import build

table = "TABLE"
value = "VALUE"

sql, params = build(lambda w: f"""
    SELECT * FROM {table}
    WHERE value = {w(value)}
""")
```

We simply pass `build` a callable that takes a `wrapper` argument. This wrapper is itself a `callable` that returns the substituted parameter name whilst simultaneously adds the value to the parameter dictionary to be returned along with the finalized SQL.

