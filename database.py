import json
import os

BASE_DIR = ".data"

class Table:
    def __init__(self,table_name,database_name,schema:dict[str,any]):
        self.path = os.path.join(BASE_DIR,database_name,table_name+".json")
        self.name = table_name
        self.schema = schema

    def load_data(self):
        self.create_if_not_exists()
        with open(self.path,"r") as f:
            data = json.load(f)
        print(type(data))
        return data

    def create_if_not_exists(self):
        if not os.path.exists(self.path):
            with open(self.path,"w") as f:
                json.dump([{}],f)

    def validate_row(self,*args):
        pass

    def save_data(self,data):
        with open(self.path,"w") as file:
            json.dump(data,file)

    def add_row(self,*args):
        self.validate_row(*args)
        data = self.load_data()
        row = {k:v for k,v in zip(self.schema.keys(),args)}
        if len(data) == 0:
            data = [row]
        else:
            data.append(row)
        self.save_data(row)


    def __str__(self):
        return ""


def create_basedir():
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)


class Database:
    def __init__(self,name):
        self.name = name
        create_basedir()
        self.create_database()

    def create_database(self):
        if not os.path.exists(os.path.join(BASE_DIR,self.name)):
            os.mkdir(os.path.join(BASE_DIR,self.name))


    def create_table(self,table_name:str,schema:dict[str,any]):
        if not os.path.exists(os.path.join(BASE_DIR,self.name,table_name)):
            os.mkdir(os.path.join(BASE_DIR,self.name,table_name))
        table = Table(table_name,self.name,schema)
        return table


