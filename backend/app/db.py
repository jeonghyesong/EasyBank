import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

#데이터베이스 url 불러옴 
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()        #모든 ORM 모델들이 상속할 공통 베이스 클래스


#실제 데이터베이스 테이블을 생성
def init_db():
    from app.models import Account, Transaction, Product, UserDeposit
    Base.metadata.create_all(bind=engine)
