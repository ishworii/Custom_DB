class DataType:
    VARCHAR = "varchar"
    INT = "int"
    TEXT = "text"
    BOOLEAN = "boolean"
    DATE = "date"


SQL_TO_PYTHON_TYPES = {
    "varchar": str,
    "text": str,
    "int": int,
    "boolean": bool,
    "date": str
}


def get_python_type(sql_type: str):
    if sql_type.lower().startswith("varchar"):
        return str
    return SQL_TO_PYTHON_TYPES.get(sql_type.lower(), str)
