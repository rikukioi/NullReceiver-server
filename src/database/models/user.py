from sqlalchemy import Column, Integer, String

from .base import BaseTable


class User(BaseTable):
    __tablename__ = "NR_USER"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(String(80), nullable=False)
