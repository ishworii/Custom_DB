from database import Table, select, Database


def pretty_print(data):
    if not data:
        print("No data to display.")
        return

    headers = data[0].keys()

    column_widths = {header: max(len(header), max(len(str(row[header])) for row in data)) for header in headers}
    header_row = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
    print(header_row)
    print("-" * len(header_row))

    for row in data:
        data_row = " | ".join(f"{str(row[header]):<{column_widths[header]}}" for header in headers)
        print(data_row)


class Query:
    current_database = None

    def __init__(self, query_string, db_name=None):
        self.query_string = query_string
        self.keywords = {"CREATE", "UPDATE", "DELETE", "SELECT", "USE"}
        self.command = None
        self.tokens = None
        self.db_name = db_name if db_name else Query.current_database
        self.parse()

    @classmethod
    def use_database(cls, db_name):
        cls.current_database = db_name

    def set_default_db(self, db_name):
        self.db_name = db_name

    def parse(self):
        tokens = self.query_string.split()
        if not tokens:
            return ValueError("Query string is empty")
        command = tokens[0].upper()
        if command not in self.keywords:
            return ValueError("Query string is invalid")
        self.command = command
        self.tokens = tokens[1:]

    def parse_delete_query(self, query_parts):
        try:
            # Expected format: FROM table_name WHERE column = value
            if query_parts[0].upper() != 'FROM':
                raise ValueError("DELETE query must start with 'FROM'")

            table_name = query_parts[1]

            # Find WHERE clause
            where_index = -1
            for i, token in enumerate(query_parts):
                if token.upper() == 'WHERE':
                    where_index = i
                    break

            if where_index == -1:
                raise ValueError("Missing WHERE clause")

            # Extract WHERE condition
            where_clause = ' '.join(query_parts[where_index + 1:])
            condition = where_clause.split('=')
            where_column = condition[0].strip()
            where_value = condition[1].strip().rstrip(';')

            return {
                'table': table_name,
                'where_column': where_column,
                'where_value': where_value
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid DELETE query format: {e}")

    def parse_update_query(self, query_parts):
        try:
            table_name = query_parts[0]

            set_index = -1
            where_index = -1
            for i, token in enumerate(query_parts):
                if token.upper() == 'SET':
                    set_index = i
                elif token.upper() == 'WHERE':
                    where_index = i

            if set_index == -1 or where_index == -1:
                raise ValueError("Missing SET or WHERE clause")

            set_clause = ' '.join(query_parts[set_index + 1:where_index])
            updates = {}
            for item in set_clause.split(','):
                column, value = [x.strip() for x in item.split('=')]
                if value.startswith('"') or value.startswith("'"):
                    value = value[1:-1]
                updates[column] = value

            where_clause = ' '.join(query_parts[where_index + 1:])
            condition = where_clause.split('=')
            where_column = condition[0].strip()
            where_value = condition[1].strip().rstrip(';')

            return {
                'table': table_name,
                'updates': updates,
                'where_column': where_column,
                'where_value': int(where_value)
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid UPDATE query format: {e}")

    def convert_value(self, value, col_type):
        if col_type.lower().startswith('varchar') or col_type.lower() == 'text':
            return str(value)
        elif col_type.lower() == 'int':
            return int(value)
        elif col_type.lower() == 'boolean':
            return bool(value.lower() == 'true')
        return value

    def execute(self):
        if self.command == "USE":
            db_name = self.tokens[0].replace(";", "")
            Query.use_database(db_name)
            print(f"Using database: {db_name}")
            return

        if self.command == "CREATE":
            sub_command = self.tokens[0].upper()
            tb_db_name = self.tokens[1].replace(";", "")
            if sub_command == "DATABASE":
                db = Database(tb_db_name)
                print(f"Creating database {tb_db_name}")
            else:
                if not self.db_name:
                    raise ValueError("No database selected. Use 'USE DATABASE' first.")
                schema_text = " ".join(self.tokens[2:])
                schema_parts = schema_text.strip("()").split(",")
                schema = {}
                for part in schema_parts:
                    col_def = part.strip().split()
                    if len(col_def) >= 2:
                        col_name = col_def[0]
                        col_type = " ".join(col_def[1:]).lower()
                        schema[col_name] = col_type

                db = Database(self.db_name)
                table = db.create_table(tb_db_name, schema)
                return table

        elif self.command == "UPDATE":
            if not self.db_name:
                raise ValueError("No database selected. Use 'USE DATABASE' first.")

            parsed = self.parse_update_query(self.tokens)
            table = Table(parsed['table'], self.db_name)
            data = table.load_data()

            updated = False
            for row in data:
                if row['id'] == parsed['where_value']:
                    for col, value in parsed['updates'].items():
                        if col not in table.schema:
                            raise ValueError(f"Column '{col}' not found in table schema")
                        converted_value = self.convert_value(value, table.schema[col])
                        row[col] = converted_value
                    updated = True
                    break

            if not updated:
                print(f"No record found with id {parsed['where_value']}")
            else:
                table.save_data(data)
                print(f"Updated record with id {parsed['where_value']}")

        elif self.command == "DELETE":
            if not self.db_name:
                raise ValueError("No database selected. Use 'USE DATABASE' first.")

            parsed = self.parse_delete_query(self.tokens)
            table = Table(parsed['table'], self.db_name)
            data = table.load_data()

            # Convert where_value to appropriate type based on schema
            where_col = parsed['where_column']
            if where_col not in table.schema and where_col != 'id':
                raise ValueError(f"Column '{where_col}' not found in table schema")

            col_type = 'int' if where_col == 'id' else table.schema[where_col]
            where_value = self.convert_value(parsed['where_value'], col_type)

            initial_length = len(data)
            data = [row for row in data if str(row[where_col]) != str(where_value)]

            if len(data) == initial_length:
                print(f"No records found matching the condition")
            else:
                table.save_data(data)
                print(f"Deleted {initial_length - len(data)} record(s)")

        elif self.command == "SELECT":
            if not self.db_name:
                raise ValueError("No database selected. Use 'USE DATABASE' first.")
            wildcard = self.tokens[0]
            table_name = self.tokens[2]
            table = Table(table_name, self.db_name)
            if wildcard == "*":
                data = select(table, wildcard=True)
                pretty_print(data)
            else:
                column_names = self.tokens[0].split(",")
                data = select(table, wildcard=False, cols=column_names)
                pretty_print(data)
