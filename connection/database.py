from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_database = 'postgresql://postgres:tejas83527@metaworkbackend.clyqy0y02fiu.us-west-1.rds.amazonaws.com:5432/metaworkBackend'
# URL_database = 'postgresql://postgres:83527@localhost:5432/metaworkBackend'

engine = create_engine(URL_database)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
