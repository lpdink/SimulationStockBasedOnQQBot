from sqlalchemy import Column, Text, DECIMAL, create_engine, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class AllStock(BASE):
    __tablename__ = 'all_stock'
    stock_id = Column(Text, primary_key=True)
    stock_name = Column(Text, primary_key=True)

    def __init__(self, stock_id, stock_name):
        self.stock_id = stock_id
        self.stock_name = stock_name