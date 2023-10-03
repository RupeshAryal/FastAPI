from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import models

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost/sqlalchemy'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()