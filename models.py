from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


class DSA(Base):
    __tablename__ = "dsa"

    id = Column(Integer, primary_key=True)
    question = Column(String)