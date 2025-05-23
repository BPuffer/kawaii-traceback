
def hello():
    print("Hello, world!")

def raise_error():
    raise Exception(f"Exception occurred in {__name__}")

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


def scipy_error():
    import scipy, numpy
    def f(x, y):
        return x * x + y * y + 1

    return scipy.optimize.minimize(f, numpy.array([1, 1, 1]))
