from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String, Integer, Boolean, Float, ForeignKey
from typing import List, Optional



class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[str] = mapped_column(Boolean, nullable=False, default=False)

    accounts: Mapped[Optional[List['Account']]] = relationship(back_populates='user', cascade='all, delete')

    def __repr__(self):
        return f'User(id={self.id}, email={self.email}, full_name={self.full_name}, is_admin={self.is_admin})'
    

class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    balance: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='accounts')
    transacts: Mapped[Optional[List['Transaction']]] = relationship(back_populates='account', cascade='all, delete')

    def __repr__(self):
        return f'Account(id={self.id}, balance={self.balance})'


class Transaction(Base):
    __tablename__ = 'transacts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unq_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'))
    amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    account: Mapped['Account'] = relationship(back_populates='transacts')

    def __repr__(self):
        return f'Transaction(id={self.id}, unq_id={self.unq_id})'