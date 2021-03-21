from sqlalchemy import Column, Text, create_engine, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class StockInformation(BASE):
    stock_id = Column(Text, primary_key=True)
    stock_name = Column(Text)
    now_price = Column(Float)
    flush_time = Column(DateTime)


if __name__ == "__main__":
    pass
