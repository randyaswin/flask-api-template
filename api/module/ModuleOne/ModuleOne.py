from api.module.ModuleOne.db.query import query


class ModuleOne:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y
    
    def subtract(self):
        return self.x - self.y
    
    def multiply(self):
        return self.x * self.y
    
    def divide(self):
        return self.x / self.y
    
    def power(self):
        return self.x ** self.y
    
    def square_root(self):
        return self.x ** (1/self.y)
    
    def getData(self, db_connection, *args, **kwargs):
        data = query(db_connection, *args, **kwargs)
        return data.to_dict(orient="records")
    