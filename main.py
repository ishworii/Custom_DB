import database



def main():
    db = database.Database("test_db")
    schema = {
        "name" : "str",
        "age" : "int",
        "sex" : "str",
        "date_of_birth" : "date",
    }
    student = db.create_table("student",schema = schema)
    student.add_row("Ishwor",21,"male","1998-05-29")
    student.add_row("Sejal",10,"female","2012-03-21")

    # student.add_row()

if __name__ == "__main__":
    main()