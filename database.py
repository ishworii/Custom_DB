import json
import os

BASE_DIR = ".data"

class Table:
    def __init__(self,table_name,database_name,schema:dict[str,any]):
        self.path = os.path.join(BASE_DIR,database_name,table_name+".json")
        self.name = table_name
        self.schema = schema
        self.id = None
        self.load_id()

    def load_id(self):
        if not os.path.exists(self.path):
            self.id = 1
            return
        with open(self.path,"r") as f:
            data = json.load(f)
        self.id = data[-1]['id'] + 1


    def load_data(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path,"r") as f:
            data = json.load(f)
        return data

    def validate_row(self,*args):
        if len(args) != len(self.schema.keys()):
            print("Invalid number of arguments")
            return False
        for col_type,each_col in zip(self.schema.values(),args):
            if not isinstance(each_col,eval(col_type)):
                print("Invalid column type")
                return False
        return True

    def save_data(self,data):
        with open(self.path,"w") as file:
            json.dump(data,file,indent=4)

    def add_row(self,*args):
        assert self.validate_row(*args) == True
        data = self.load_data()
        row = {k:v for k,v in zip(self.schema.keys(),args)}
        row['id'] = self.id
        self.id += 1
        if len(data) == 0:
            data = [row]
        else:
            data.append(row)
        self.save_data(data)

    def update_row(self,pk,*args):
        print("update row",pk,args)
        assert self.validate_row(*args) == True
        if pk > self.id:
            print("Invalid ID")
            return
        data = self.load_data()
        for index,each_row in enumerate(data):
            if pk == each_row['id']:
                print("update row",pk,each_row)
                each_row = {k:v for k,v in zip(each_row.keys(),args)}
                each_row['id'] = pk
                data[index] = each_row
                break
        self.save_data(data)

    def delete_row(self,pk):
        assert pk <= self.id
        data = self.load_data()
        data = [d for d in data if d['id'] != pk]
        self.save_data(data)

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


