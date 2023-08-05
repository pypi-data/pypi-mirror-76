# `lonny_common_pg`

A quality-of-life wrapper for the psycopg2 connection object.

## Installation

```bash
pip install lonny_common_pg
```

## Usage

To import the connection object, simply do:

```python
from lonny_common_pg import Connection
```

 - The connection object constructor takes `host`, `port`, `dbname`, `user` and `password` kwargs.
 - The connection isn't initialized until a query is made or `init` is explicitly called.
 - The connection can be closed by using `close` - however it can be subsequently re-opened at anytime. When used in a `with` contextmanager context - the connection is closed when leaving the block.
 - The 3 methods for querying the database are: `execute`, `fetch_one` and `fetch_all`. All of these can either take a SQL string, or a callable (see the `lonny_sql` module for usage).
 - This connection wrapper uses `autocommit` mode and the `DictCursor` for returning results.

 ### Nested Transactions

Nested transactions are possible using this library. The outermost transaction uses a standard `TRANSACTION` construct. Inner transactions use a `SAVEPOINT` instead.

```python
conn = Connection(**kwargs)
with conn.transaction():
    try:
        do_something_else()
        with conn.transaction():
            do_something()
    except:
        pass
```

