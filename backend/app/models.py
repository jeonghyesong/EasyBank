import enum
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    ForeignKey, Enum as SQLEnum, Text
)
from sqlalchemy.orm import relationship
from .database import Base

#사용자 (예금주)
class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(100), nullable=False, unique=True)  # 예금주 이름
    password = Column(String(20), nullable=False)                # 전체 서비스용 비밀번호

    accounts = relationship("Account", back_populates="owner")

#계좌
class Account(Base):
    __tablename__ = "accounts"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    nickname     = Column(String(50), nullable=True)     # 계좌 별칭
    balance      = Column(Float, default=0.0, nullable=False)
    account_type = Column(String(20), default="checking", nullable=False)
    created_at   = Column(DateTime, default=datetime.datetime.utcnow)

    owner        = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    deposits     = relationship("UserDeposit", back_populates="account")

#거래 종류
class TransactionType(enum.Enum):
    DEPOSIT    = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER   = "transfer"

#거래 내역
class Transaction(Base):
    __tablename__ = "transactions"
    id          = Column(Integer, primary_key=True, index=True)
    account_id  = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    type        = Column(SQLEnum(TransactionType), nullable=False)
    amount      = Column(Float, nullable=False)
    timestamp   = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String(255), default="")

    account     = relationship("Account", back_populates="transactions")

#상품 설명 (예금·적금·대출·카드)
class Product(Base):
    __tablename__ = "products"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

#사용자 예금/적금 가입 정보
class UserDeposit(Base):
    __tablename__ = "user_deposits"
    id           = Column(Integer, primary_key=True, index=True)
    account_id   = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=False)
    principal    = Column(Float, nullable=False)
    opened_at    = Column(DateTime, default=datetime.datetime.utcnow)
    maturity_at  = Column(DateTime, nullable=False)
    monthly_limit = Column(Float, nullable=True)

    account      = relationship("Account", back_populates="deposits")
    product      = relationship("Product")