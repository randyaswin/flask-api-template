from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ModuleOne(Base):
    __tablename__ = "module_one"
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    result = Column(Integer)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        self.result = self.x + self.y
        return self.result

    def subtract(self):
        self.result = self.x - self.y
        return self.result

    def __repr__(self):
        return "<ModuleOne(x='%s', y='%s', result='%s')>" % (
            self.x,
            self.y,
            self.result,
        )

