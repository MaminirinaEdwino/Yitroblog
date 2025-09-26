
from fastapi import Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import setting	
DATABASE_URL = f'postgresql://{setting.db_username}:{setting.db_password}@localhost:5432/{setting.db_name}'


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()
       
db_dependency = Depends(get_db)
	
