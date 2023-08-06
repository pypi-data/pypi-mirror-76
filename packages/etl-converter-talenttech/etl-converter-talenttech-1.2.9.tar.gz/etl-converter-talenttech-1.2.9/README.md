ETL table converter and creator
==========

The Python Toolkit for converting table from one database to another

Databases types
-------------

Supported databases. You have to use short name of database
short_name:type of database 
* ch:clickhouse
* pg:postgresql
* mysql:mysql
* vertica:vertica
* exasol:exasol


Supported database conversions
-------------
* mysql to pg
* mysql to vertica
* mysql to exasol
* ch to vertica
* pg to vertica


Credentials
-------------
```sh
sql_credentials = {
    "pg": {
        "database": os.getenv("PG_DATABASE"),
        "schema": os.getenv("PG_SCHEMA"),
        "user": os.getenv("PG_USER"),
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
        "password": os.getenv("PG_PASSWORD"),
        #additional params bellow (optional) 
        "executemany_mode": "values",
        "executemany_values_page_size": 10000,
        "executemany_batch_page_size": 500,
    },
    "ch": {
        "database": os.getenv("CH_DATABASE"),
        "user": os.getenv("CH_USER"),
        "host": os.getenv("CH_HOST"),
        "port": os.getenv("CH_PORT"),
        "password": os.getenv("CH_PASSWORD"),
        #additional params bellow (optional) 
        "connect_args": {
            "alt_hosts": "{},{}:{}".format(
                os.getenv("CH_HOST_B"), os.getenv("CH_HOST_C"), os.getenv("CH_PORT")
            )
        },
    },
    "vertica": {
        "database": os.getenv("VERTICA_DATABASE"),
        "schema": os.getenv("VERTICA_SCHEMA"),
        "user": os.getenv("VERTICA_USER"),
        "host": os.getenv("VERTICA_HOST"),
        "port": os.getenv("VERTICA_PORT"),
        "password": os.getenv("VERTICA_PASSWORD"),
        #additional params bellow (optional) 
        "connect_args": {
            "connection_load_balance": True,
            "backup_server_node": json.loads(os.getenv("VERTICA_CONFIGS"))[
                "backup_server_node"
            ],
        },
    },
    "mysql": {
        "database": os.getenv("MYSQL_DATABASE"),
        "user": os.getenv("MYSQL_USER"),
        "host": os.getenv("MYSQL_HOST"),
        "port": os.getenv("MYSQL_PORT"),
        "password": os.getenv("MYSQL_PASSWORD"),
    },
}
```

Usage
```sh
pip3 install etl-converter-talenttech
```

```python
import os
from converter.fields_converter import FieldsConverter

tables = [
    "directions",
    "users"
]
from_db = "mysql"
to_db = "pg"
converter = FieldsConverter(sql_credentials, from_db, to_db, tables=tables)

print(converter.get_columns(tables[0]))
print(converter.get_columns(tables[0], table_from=False))
print(converter.create_list_of_tables(tables, to_create=False, dir=None))