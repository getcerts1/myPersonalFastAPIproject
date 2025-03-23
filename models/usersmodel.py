from db.database import Base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql import func



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    time_created = Column(TIMESTAMP, nullable=False, server_default=func.now())



