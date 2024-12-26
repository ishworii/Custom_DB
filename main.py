import query


# def main():
#     # First create and populate the table
#     query.Query("CREATE DATABASE TestDB;").execute()
#     query.Query("USE TestDB;").execute()
#
#     # Create table
#     create_query = """
#     CREATE TABLE Persons (
#         PersonID INT,
#         LastName VARCHAR(255),
#         FirstName VARCHAR(255),
#         Address TEXT,
#         Active BOOLEAN
#     );
#     """
#     tb = query.Query(create_query).execute()
#
#     # Add initial data
#     tb.add_row(1, "Doe", "John", "123 Main St", True)
#     tb.add_row(1, "Khanal", "Ishwor", "25 mirage", True)
#     tb.add_row(1, "Khanal", "Sejal", "Pharsatikar", True)
#
#     # Update the record
#     update_query = """
#     UPDATE Persons
#     SET LastName = "Smith", FirstName = "Jane"
#     WHERE id = 1;
#     """
#     query.Query(update_query).execute()
#
#     # View the results
#     query.Query("SELECT * FROM Persons").execute()

def main():
    query.Query("USE TestDB;").execute()
    query.Query("SELECT * FROM Persons").execute()

    # Delete a record
    delete_query = "DELETE FROM Persons WHERE id = 1;"
    query.Query(delete_query).execute()

    # Verify the deletion
    query.Query("SELECT * FROM Persons").execute()


if __name__ == "__main__":
    main()
