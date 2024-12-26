# CustomDB - A JSON-based Database Implementation

CustomDB is a lightweight, JSON-based database implementation in Python that supports basic SQL-like operations. It
provides a simple way to create databases and tables, and perform CRUD operations using familiar SQL syntax.

## Features

- Database and table creation
- SQL-like query syntax
- Data persistence using JSON files
- Support for multiple data types
- CRUD Operations (Create, Read, Update, Delete)
- Pretty-printed query results

## Installation

1. Clone the repository:

```bash
git clone git@github.com:ishworii/Custom_DB.git
cd Custom_DB
```

## Usage

### Basic Database Operations

```python
from query import Query

# Create a new database
Query("CREATE DATABASE TestDB;").execute()

# Use the database
Query("USE TestDB;").execute()
```

### Creating Tables

```python
# Create a table with specified schema
create_query = """
CREATE TABLE Persons (
    PersonID INT,
    LastName VARCHAR(255),
    FirstName VARCHAR(255),
    Address TEXT,
    Active BOOLEAN
);
"""
table = Query(create_query).execute()
```

### Adding Data

```python
# Add data to table using the table object
table.add_row(1, "Doe", "John", "123 Main St", True)
table.add_row(2, "Smith", "Jane", "456 Oak St", True)
```

### Querying Data

```python
# Select all columns
Query("SELECT * FROM Persons").execute()

# Select specific columns
Query("SELECT FirstName,LastName FROM Persons").execute()
```

### Updating Data

```python
# Update records
update_query = """
UPDATE Persons 
SET LastName = "Smith", FirstName = "Jane" 
WHERE id = 1;
"""
Query(update_query).execute()
```

### Deleting Data

```python
# Delete records
Query("DELETE FROM Persons WHERE id = 1;").execute()
```

## Data Types

The database supports the following data types:

- INT
- VARCHAR
- TEXT
- BOOLEAN

## Project Structure

```
customdb/
├── database.py      # Core database and table operations
├── query.py         # Query parsing and execution
└── main.py         # Example usage
```

## Technical Details

### Storage Format

- Databases are represented as directories under `.data/`
- Tables are stored as JSON files within their database directory
- Each table has an associated schema file

### Data Structure

Tables are stored in JSON format:

```json
[
  {
    "id": 1,
    "FirstName": "John",
    "LastName": "Doe",
    "Address": "123 Main St",
    "Active": true
  },
  {
    "id": 2,
    "FirstName": "Jane",
    "LastName": "Smith",
    "Address": "456 Oak St",
    "Active": true
  }
]
```

## Query Syntax

### CREATE

```sql
CREATE
DATABASE database_name;
CREATE TABLE table_name
(
    column1 datatype,
    column2 datatype, .
    .
    .
);
```

### SELECT

```sql
SELECT *
FROM table_name;
SELECT column1, column2
FROM table_name;
```

### UPDATE

```sql
UPDATE table_name
SET column1 = value1,
    column2 = value2
WHERE id = value;
```

### DELETE

```sql
DELETE
FROM table_name
WHERE column = value;
```

## Error Handling

The implementation includes error handling for:

- Invalid database/table names
- Schema validation
- Data type validation
- Missing database context
- Invalid query syntax

## Limitations

- No support for JOIN operations
- Limited WHERE clause functionality
- No indexing support
- Basic data types only
- Single-user operation

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
