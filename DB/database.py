from sqlalchemy import create_engine, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = 'database.sqlite'

engine = create_engine(f'sqlite:///{db_name}')
session = sessionmaker(bind=engine)

base = declarative_base()


def create_db():
    base.metadata.create_all(engine)