class Query:
    def __init__(self,query_string):
        self.query_string = query_string
        self.keywords = ("create","update","delete","select","where","*")

    def parse(self):
        pass

    def validate(self):
        pass

    def execute(self):
        pass


