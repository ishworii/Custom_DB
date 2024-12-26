import json
import os
from datatypes import get_python_type

BASE_DIR = ".data"


class Table:
    def __init__(self, table_name, database_name, schema: dict[str, any] = None):
        if not database_name:
            raise ValueError("No database specified")
        self.path = os.path.join(BASE_DIR, database_name, f"{table_name}.json")
        self.name = table_name
        self.schema = schema
        self.schema_path = os.path.join(BASE_DIR, database_name, f"{table_name}_schema.json")
        self.id = None
        if schema:
            self.save_schema()
        else:
            self.load_schema()
        self.initialize_table()
        self.load_id()

    def save_schema(self):
        with open(self.schema_path, "w") as f:
            json.dump(self.schema, f, indent=4)

    def load_schema(self):
        try:
            with open(self.schema_path, "r") as f:
                self.schema = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Schema not found for table {self.name}")

    def initialize_table(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            self.save_data([])

    def load_data(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data

    def save_data(self, data):
        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)

    def load_id(self):
        data = self.load_data()
        self.id = data[-1]['id'] + 1 if data else 1

    def validate_row(self, *args):
        if len(args) != len(self.schema.keys()):
            print("Invalid number of arguments")
            return False

        for (col_name, col_type), value in zip(self.schema.items(), args):
            python_type = get_python_type(col_type)
            try:
                if not isinstance(value, python_type):
                    converted_value = python_type(value)
            except ValueError:
                print(f"Invalid value for column {col_name}: expected {col_type}")
                return False
        return True

    def add_row(self, *args):
        assert self.validate_row(*args) == True
        data = self.load_data()
        row = {k: v for k, v in zip(self.schema.keys(), args)}
        row['id'] = self.id
        self.id += 1
        if len(data) == 0:
            data = [row]
        else:
            data.append(row)
        self.save_data(data)

    def update_row(self, pk, *args):
        print("update row", pk, args)
        assert self.validate_row(*args) == True
        if pk > self.id:
            print("Invalid ID")
            return
        data = self.load_data()
        for index, each_row in enumerate(data):
            if pk == each_row['id']:
                print("update row", pk, each_row)
                each_row = {k: v for k, v in zip(each_row.keys(), args)}
                each_row['id'] = pk
                data[index] = each_row
                break
        self.save_data(data)

    def delete_row(self, pk):
        assert pk <= self.id
        data = self.load_data()
        data = [d for d in data if d['id'] != pk]
        self.save_data(data)

    def __str__(self):
        return ""


def select(table: Table, wildcard=True, cols=None):
    data = table.load_data()
    if wildcard:
        return data
    else:
        res = []
        for each_row in data:
            res.append({k: v for k, v in each_row.items() if k in cols})
        return res


def create_basedir():
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)


class Database:
    def __init__(self, name):
        self.name = name
        create_basedir()
        self.create_database()

    def create_database(self):
        if not os.path.exists(os.path.join(BASE_DIR, self.name)):
            os.mkdir(os.path.join(BASE_DIR, self.name))

    def create_table(self, table_name: str, schema: dict[str, any]):
        table = Table(table_name, self.name, schema)
        return table
