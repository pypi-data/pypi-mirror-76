import logging
import sys
import warnings
import json
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

warnings.filterwarnings("ignore")

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.ERROR,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.captureWarnings(True)

types_converter_dict = {
    "mysql:pg": {
        "type": {
            "char": "character",
            "varchar": "character varying",
            "tinytext": "text",
            "mediumtext": "text",
            "text": "text",
            "longtext": "text",
            "tinyblob": "bytea",
            "mediumblob": "bytea",
            "longblob": "bytea",
            "binary": "bytea",
            "varbinary": "bytea",
            "bit": "bit varying",
            "tinyint": "smallint",
            "tinyint unsigned": "smallint",
            "smallint": "smallint",
            "smallint unsigned": "integer",
            "mediumint": "integer",
            "mediumint unsigned": "integer",
            "int": "integer",
            "int unsigned": "bigint",
            "bigint": "bigint",
            "bigint unsigned": "numeric",
            "float": "real",
            "float unsigned": "real",
            "double": "double precision",
            "double unsigned": "double precision",
            "decimal": "numeric",
            "decimal unsigned": "numeric",
            "numeric": "numeric",
            "numeric unsigned": "numeric",
            "date": "date",
            "datetime": "timestamp without time zone",
            "time": "time without time zone",
            "timestamp": "timestamp without time zone",
            "year": "smallint",
            "enum": "character varying",
            "set": "ARRAY[]::text[]",
        },
        "default": {"current_timestamp": "now()"},
    },
    "mysql:vertica": {
        "type": {
            "text": "long varchar(65000)",
            "json": "long varchar(65000)",
            "enum": "long varchar",
            "double": "double precision",
        },
        "default": {"current_timestamp": "now()", "'0000-00-00 00:00:00'": "null"},
    },
    "mysql:exasol": {
        "type": {
            "text": "varchar",
            "json": "varchar",
            "enum": "varchar",
            "blob": "varchar",
            "set": "varchar",
            "tinytext": "varchar",
            "datetime": "timestamp",
        },
        "default": {},
    },
    "ch:vertica": {
        "type": {
            "string": "long varchar(65000)",
            "uuid": "long varchar(65000)",
            "double": "double precision",
            "uint8": "integer",
            "uint16": "integer",
            "uint32": "integer",
            "uint64": "integer",
            "int64": "integer",
            "int8": "integer",
            "int16": "integer",
            "int32": "integer",
            "array(string)": "array[varchar(100)]",
        },
        "default": {},
    },
    "pg:vertica": {
        "type": {
            "_text": "long varchar(65000)",
            "text": "long varchar(65000)",
            "jsonb": "long varchar(65000)",
            "json": "long varchar(65000)",
            "int2": "bigint",
            "int4": "bigint",
            "int8": "bigint",
            "float4": "double precision",
            "float8": "double precision",
            "numeric": "numeric precision",
        },
        "default": {},
    },
}

dialect_dict = {
    "ch": "clickhouse+native",
    "pg": "postgresql",
    "mysql": "mysql+pymysql",
    "vertica": "vertica+vertica_python",
    "exasol": "exa+pyodbc",
}

quotes_dict = {
    "ch": "`",
    "pg": '"',
    "mysql": '"',
    "vertica": '"',
    "exasol": '"',
}

max_length_mult = {
    "ch": 1,
    "pg": 1,
    "mysql": 1,
    "vertica": 1.8,
    "exasol": 1,
}

python_type_dict = {
    "ch": {
        "str": "Nullable(String)",
        "bool": "UInt8",
        "int": "UInt32",
        "float": "float",
    },
    "pg": {},
    "mysql": {},
    "vertica": {
        "str": "long varchar(1000)",
        "int": "bigint",
        "bool": "boolean",
        "float": "double precision",
    },
    "exasol": {},
}

# types update to insert then
update_types_dict = {
    "ch": {
        "str": "str",
        "float": "float",
        "uint8": "bool",
        "uint16": "int",
        "uint32": "int",
        "uint64": "int",
        "int8": "int",
        "int16": "int",
        "int32": "int",
        "int64": "int",
    },
    "pg": {
        "double precision": "float",
        "integer": "int",
        "json": "json",
        "boolean": "bool",
    },
    "mysql": {
        "double precision": "float",
        "int": "int",
        "json": "json",
        "boolean": "bool",
    },
    "vertica": {
        "double precision": "float",
        "integer": "int",
        "json": "json",
        "boolean": "bool",
    },
    "exasol": {
        "double precision": "float",
        "integer": "int",
        "json": "json",
        "boolean": "bool",
    },
}


def update_value_type(fields, item, key, db="ch", dict_replace_str={}):
    """
    :param db: db to update
    :param fields: dict - key  type
    :param item: - to upldate item
    :param key: key to updatee
    :return:
    """
    if db not in dialect_dict:
        raise ModuleNotFoundError(
            "Dialect for {} type of database was'nt found, should be in list {}".format(
                db, list(dialect_dict.keys())
            )
        )
    if item is None:
        return item
    if key not in item:
        return item
    if item[key] is None:
        return item
    type = "str"
    for type_old in update_types_dict[db]:
        if fields[key].lower().find(type_old) > -1:
            type = update_types_dict[db][type_old]

    if type == "int":
        item[key] = int(item[key])
    elif type == "float":
        item[key] = float(item[key])
    elif type == "json":
        item[key] = json.dumps(item[key])
    elif type == "bool":
        item[key] = bool(item[key])
    else:
        item[key] = str(item[key])
        for key_replace in dict_replace_str:
            item[key] = item[key].replace(key_replace, dict_replace_str[key_replace])
    return item


excluded_fields = ["password"]


def update_column_type(column, from_db, to_db):
    """convert types between source and destination"""
    key = "{}:{}".format(from_db, to_db)
    if key not in types_converter_dict:
        raise NotImplementedError(
            "table converter from {} to {} is not implemented".format(from_db, to_db)
        )

    type_from = column["data_type"]
    types_conv = types_converter_dict[key]["type"]
    if type_from in types_conv:
        type_to = types_conv[type_from]
    else:
        type_to = type_from

    if column["character_maximum_length"] is not None and type_to not in "text":
        type_to += "({character_maximum_length})".format(
            character_maximum_length=int(
                column["character_maximum_length"] * max_length_mult[to_db]
            )
        )
        return type_to
    if column["column_default"] is not None:
        default_from = column["column_default"].lower()
        if default_from in types_converter_dict[key]["default"]:
            default_to = types_converter_dict[key]["default"][default_from]
        else:
            default_to = default_from
        type_to += " default {column_default}".format(column_default=default_to)

    return type_to


def generate_sort_part_vertica(sort_part, date_field="date"):
    part = (
        "PARTITION BY EXTRACT(year FROM {date_field}) * 10000 + EXTRACT(MONTH FROM {date_field}) * 100 + EXTRACT("
        "day FROM {date_field})".format(date_field=date_field)
    )
    sort_field = sort_part[0]["SORTING_KEY"]
    if sort_field != "":
        sort = "ORDER BY {sort_field}".format(sort_field=sort_field)
    else:
        sort = ""
    return sort + " " + part


def get_type_sql_alchemy(type):
    try:
        return str(type.nested_type.__visit_name__).lower()
    except BaseException:
        return str(type.__visit_name__).lower()


def get_length_type_sql_alchemy(type):
    try:
        return type.length
    except BaseException:
        None


def get_default_arg_sql_alchemy(column):
    if column.default is not None:
        return column.default.arg
    elif column.server_default is not None:
        return str(column.server_default.arg)


def get_table_schema(table_name, meta):
    columns_name = [
        "column_name",
        "data_type",
        "character_maximum_length",
        "column_default",
    ]
    table_sql = Table(table_name, meta)
    columns = [c.name for c in table_sql.columns]
    types = [get_type_sql_alchemy(c.type) for c in table_sql.columns]
    length = [get_length_type_sql_alchemy(c.type) for c in table_sql.columns]
    default = [get_default_arg_sql_alchemy(c) for c in table_sql.columns]
    fields = list(zip(columns, types, length, default))
    fields = [dict(zip(columns_name, f)) for f in fields]
    return fields


class FieldsConverterOneWay:
    """
    class to upload just one way
    """

    def __init__(self, sql_credentials, db, debug=True, tables=None):
        """

        :param sql_credentials:
        :param db:
        :param debug: show debug text
        :param tables:  converter only for list of tables. Will process more rapid
        """

        self.tables = tables or []
        self.db = db
        self.debug = debug
        self.sql_credentials = sql_credentials
        self.cred = self.sql_credentials[self.db]

        if self.db not in dialect_dict:
            raise ModuleNotFoundError(
                "Dialect for {} type of database was'nt found, should be in list {}".format(
                    self.db, list(dialect_dict.keys())
                )
            )
        else:
            dialect_from = dialect_dict[self.db]
        uri_sql_alchemy = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            dialect_from,
            self.cred["user"],
            self.cred["password"],
            self.cred["host"],
            self.cred["port"],
            self.cred["database"],
        )
        additional_args = {}
        for key in self.sql_credentials[self.db]:
            if key not in ["database", "schema", "user", "host", "password", "port"]:
                additional_args[key] = self.sql_credentials[self.db][key]
        self.engine = create_engine(uri_sql_alchemy, **additional_args)
        self.conn = self.engine.connect()
        self.log("connecting to {} successfull".format(self.db))
        self.quote_char = quotes_dict[self.db]
        self.init_meta()

    def init_meta(self, tables=None):
        """
        reinit meta objects
        :return:
        """
        if "schema" in self.cred:
            self.schema = self.cred["schema"]
            self.meta = MetaData(bind=self.engine, schema=self.schema)
        else:
            self.meta = MetaData(bind=self.engine)
            self.schema = self.cred["database"]

        tables = tables or self.tables
        if len(tables) > 0:
            self.meta.reflect(only=tables)
        else:
            self.meta.reflect()

    def log(self, text):
        if self.debug:
            logging.info(self.__str__ + ": " + text)

    def check_if_table_availible(self, table):
        if len(self.tables) > 0 and table not in self.tables:
            raise ModuleNotFoundError(
                "Table_name to convert {} should be in list{} or set tables param to defult".format(
                    table, self.tables
                )
            )

    @property
    def __str__(self):
        return "FieldsConverterOneWay_{}".format(self.db)

    @property
    def __repr__(self):
        return "FieldsConverterOneWay_{}".format(self.db)

    def __del__(self):
        self.conn.close()

    def update_value_df_type(self, table_name, dataframe, db="ch", dict_replace_str={}):
        """
        :param fields:
        :param dataframe:
        :param db:
        :param dict_replace_str:
        :return:
        """
        if db not in dialect_dict:
            raise ModuleNotFoundError(
                "Dialect for {} type of database was'nt found, should be in list {}".format(
                    db, list(dialect_dict.keys())
                )
            )
        fields = self.get_columns(table_name)
        for key in list(dataframe.columns):
            type = "str"
            for type_old in update_types_dict[db]:
                if fields[key].lower().find(type_old) > -1:
                    type = update_types_dict[db][type_old]

            dataframe[key] = dataframe[key].astype(type)
            if type == "str":
                dataframe[key] = dataframe[key].replace(to_replace=dict_replace_str)
        return dataframe

    def update_value_type(self, table_name, items, dict_replace_str={}):
        """
        :param dict_replace_str: replace in string dict
        :param items: list of dicts to update
        :param table_name: table_name to insert
        :return:
        """
        fields = self.get_columns(table_name=table_name)
        if len(fields) == 0:
            raise Exception("No table {} in metadata".format(table_name))
        keys = fields.keys()
        for item in items:
            for key in keys:
                item = update_value_type(
                    fields, item, key, db=self.db, dict_replace_str=dict_replace_str
                )
        return items

    def get_columns(self, table_name):
        """get column:type dict"""
        self.check_if_table_availible(table_name)
        fields = get_table_schema(table_name, self.meta)
        columns = [
            f["column_name"] for f in fields if f["column_name"] not in excluded_fields
        ]
        types = [
            f["data_type"] for f in fields if f["column_name"] not in excluded_fields
        ]
        return dict(zip(columns, types))

    def create_table(self, fields_python, table_name, to_create=True, dir=None):
        """create tables using python types"""
        txt = "CREATE TABLE IF NOT EXISTS {schema}.{table} (".format(
            schema=self.schema, table=table_name
        )
        types_conv = python_type_dict[self.db]
        res_list = []
        for field in fields_python:
            type_python = fields_python[field]
            if type_python in types_conv:
                type_sql = types_conv[type_python]
            else:
                type_sql = types_conv["str"]
            res_list.append(self.quote_char + field + self.quote_char + " " + type_sql)
        txt += ",".join(res_list)
        txt += ")"
        if to_create:
            self.conn.execute(txt)
            logging.info("creating table {} is successfull".format(table_name))
        if dir is not None:
            f = open(
                dir
                + "/"
                + self.schema
                + "_"
                + table_name.replace("_date", "")
                + ".sql",
                "w",
            )
            f.write(txt)
            f.close()
        return txt


class FieldsConverter:
    def __init__(self, sql_credentials, from_db, to_db, debug=True, tables=None):
        """

        :param sql_credentials:
        :param from_db:
        :param to_db:
        :param debug: show debug text
        :param tables: converter only for list of tables. Will process more rapidly
        """
        self.tables = tables or []
        self.from_db = from_db
        self.to_db = to_db
        self.debug = debug
        self.sql_credentials = sql_credentials

        self.cred_from = self.sql_credentials[self.from_db]

        if self.from_db not in dialect_dict:
            raise ModuleNotFoundError(
                "Dialect for {} type of database was'nt found, should be in list {}".format(
                    self.from_db, list(dialect_dict.keys())
                )
            )
        else:
            dialect_from = dialect_dict[self.from_db]

        uri_sql_alchemy_from = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            dialect_from,
            self.cred_from["user"],
            self.cred_from["password"],
            self.cred_from["host"],
            self.cred_from["port"],
            self.cred_from["database"],
        )
        self.cred_to = self.sql_credentials[self.to_db]
        if self.to_db not in dialect_dict:
            raise ModuleNotFoundError(
                "Dialect for {} type of database was'nt found, should be in list {}".format(
                    self.to_db, list(dialect_dict.keys())
                )
            )
        else:
            dialect_to = dialect_dict[self.to_db]

        uri_sql_alchemy_to = "{0}://{1}:{2}@{3}:{4}/{5}".format(
            dialect_to,
            self.cred_to["user"],
            self.cred_to["password"],
            self.cred_to["host"],
            self.cred_to["port"],
            self.cred_to["database"],
        )
        self.quote_char = quotes_dict[self.to_db]
        additional_args = {}
        for key in self.sql_credentials[self.from_db]:
            if key not in ["database", "schema", "user", "host", "password", "port"]:
                additional_args[key] = self.sql_credentials[self.from_db][key]
        self.engine_from = create_engine(uri_sql_alchemy_from, **additional_args)
        self.conn_from = self.engine_from.connect()
        self.log("connecting to {} successfull".format(self.from_db))
        additional_args = {}
        for key in self.sql_credentials[self.to_db]:
            if key not in ["database", "schema", "user", "host", "password", "port"]:
                additional_args[key] = self.sql_credentials[self.to_db][key]
        self.engine_to = create_engine(uri_sql_alchemy_to, **additional_args)
        self.conn_to = self.engine_to.connect()
        self.log("connecting to {} successfull".format(self.to_db))
        self.init_meta(tables=self.tables)

    def init_meta(self, tables=None):
        """

        :param tables:
        :return:
        """

        if "schema" in self.cred_from:
            self.schema_from = self.cred_from["schema"]
            self.meta_from = MetaData(bind=self.engine_from, schema=self.schema_from)
        else:
            self.meta_from = MetaData(bind=self.engine_from)

        if "schema" in self.cred_to:
            self.schema_to = self.cred_to["schema"]
            self.meta_to = MetaData(bind=self.engine_to, schema=self.schema_to)
        else:
            self.meta_to = MetaData(bind=self.engine_to)

        tables = tables or self.tables
        if len(tables) > 0:
            try:
                self.meta_from.reflect(only=tables)
            except sqlalchemy.exc.InvalidRequestError:
                raise sqlalchemy.exc.InvalidRequestError(
                    "One or more file didn't find in database {}. Critical exception"
                )
            try:
                self.meta_to.reflect(only=tables)
            except sqlalchemy.exc.InvalidRequestError:
                self.log(
                    "One or more file didn't find in database {}. Load table later".format(
                        self.to_db
                    )
                )
                self.meta_to = None
        else:
            self.meta_from.reflect()
            self.meta_to.reflect()

    def log(self, text):
        if self.debug:
            logging.info(self.__str__ + ": " + text)

    def check_if_table_availible(self, table):
        if len(self.tables) > 0 and table not in self.tables:
            raise ModuleNotFoundError(
                "Table_name to convert {} should be in list{} or set tables param to defult".format(
                    table, self.tables
                )
            )

    @property
    def __str__(self):
        return "FieldsConverter_{}_{}".format(self.from_db, self.to_db)

    @property
    def __repr__(self):
        return "FieldsConverter_{}_{}".format(self.from_db, self.to_db)

    def __del__(self):
        self.conn_from.close()
        self.conn_to.close()

    def update_value_type(self, table_name, items):
        """
        :param items: list of dicts to update
        :param table_name: table_name to insert
        :return:
        """
        fields = self.get_columns(table_name=table_name, table_from=False)
        keys = fields.keys()
        for item in items:
            for key in keys:
                item = update_value_type(fields, item, key, db=self.to_db)
        return items

    def generate_create(self, fields, table_name, sort_part=None):
        add_part = ""
        if self.schema_to:
            cur_schema = self.schema_to
        else:
            cur_schema = ""
        if self.to_db == "vertica":
            if "date" in [f.lower() for f in fields.keys()]:
                date_field = "date"
            else:
                date_field = ""
            if sort_part is not None:
                add_part = generate_sort_part_vertica(sort_part, date_field=date_field)
                if (
                        date_field != ""
                        and fields[date_field].lower().find("not null") == -1
                ):
                    fields[date_field] += " not null"
        elif self.to_db == "exasol":
            cur_schema = self.exasol_schema
        txt = "CREATE TABLE IF NOT EXISTS {schema}.{table}\n(\n".format(
            schema=cur_schema, table=table_name
        )

        txt += ",\n".join(
            [
                "    " + self.quote_char + field + self.quote_char + " " + str(fields[field])
                for field in fields
                if field not in excluded_fields
            ]
        )
        txt += "\n)"

        return txt + " " + add_part

    def get_partition_and_sort_keys_ch(self, table_name):
        columns = ["PARTITION_KEY", "SORTING_KEY", "ENGINE"]
        sql = """SELECT partition_key, 
                        sorting_key,
                        engine
                        FROM system.tables
                        WHERE name = '{table_name}'
                              AND database = '{database}'
              """.format(
            table_name=table_name, database=self.ch_database
        )
        rows = self.conn_from.execute(sql)
        if rows[0][2] == "MaterializedView":
            return self.get_partition_and_sort_keys_ch(".inner." + table_name)
        else:
            return [dict(zip(columns, r)) for r in rows]

    def get_columns(self, table_name, table_from=True):
        """get column:type dict"""
        self.check_if_table_availible(table_name)
        if table_from:
            fields = get_table_schema(table_name, self.meta_from)
        else:
            fields = get_table_schema(table_name, self.meta_to)
        columns = [
            f["column_name"] for f in fields if f["column_name"] not in excluded_fields
        ]
        types = [
            f["data_type"] for f in fields if f["column_name"] not in excluded_fields
        ]
        return dict(zip(columns, types))

    def create_ddl(self, table_name):
        sort_part = None
        self.check_if_table_availible(table_name)
        fields = get_table_schema(table_name, self.meta_from)
        fields_new = {}
        for f in fields:
            fields_new[f["column_name"]] = update_column_type(
                f, self.from_db, self.to_db
            )
        return self.generate_create(
            fields_new, table_name.replace("_data", ""), sort_part
        )

    def drop_list_of_tables(self, tables):
        """drop every fkn table in list"""
        for table in tables:
            sql = "drop table {schema}.{table} cascade ".format(
                schema=self.schema_to, table=table
            )
            self.conn_to.execute(sql)

    def create_list_of_tables(self, tables, to_create=True, dir=None):
        result_list = []
        for table in tables:
            sql = self.create_ddl(table_name=table)
            result_list.append(sql)
            if to_create:
                self.conn_to.execute(sql)
                logging.info("creating table {} is successfull".format(table))
            if dir is not None:
                f = open(
                    dir
                    + "/"
                    + self.schema_to
                    + "_"
                    + table.replace("_date", "")
                    + ".sql",
                    "w",
                )
                f.write(sql)
                f.close()
        if to_create:
            self.init_meta()
        return result_list
