from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from models.database import async_session_maker
from models.models import User, Account, Transaction
from models.auth import get_password_hash

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        '''
            Find element by index
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        '''
            Find element by criterious
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        '''
            Find all elements by criterious
        '''
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def add(cls, **values):
        '''
            Add element 
        '''
        async with async_session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance


class UserDAO(BaseDAO):
    model = User
        
    @classmethod
    async def find_all_without_filter(cls):
        '''
            Find all elements
        '''
        async with async_session_maker() as session:
            query = select(cls.model).join(cls.model.accounts).join(Account.transacts)
            result = await session.execute(query)
            return result.all()
        
    @classmethod
    async def check_admin(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user.is_admin
        
    @classmethod
    async def delete_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            user = await session.get(cls.model, data_id)
            await session.delete(user)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return True
        
    @classmethod
    async def update_by_id(cls, data_id: int, item):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            user.email = item.email
            user.full_name = item.full_name
            user.is_admin = item.is_admin
            user.password = get_password_hash(item.password)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return True

    @classmethod
    async def update_account_transaction(cls, user_id, account_id, amount, unq_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                return None
            
            query = select(Account).filter_by(id=account_id)
            result = await session.execute(query)
            account = result.scalar_one_or_none()
            if account.user_id != user.id:
                return None

            if not account:
                acc = Account(balance=amount, user_id=user_id, transacts=[Transaction(unq_id=unq_id, account_id=account_id, amount=amount)])
                session.add(acc)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return user
            
            query = select(Transaction).filter_by(unq_id=unq_id)
            result = await session.execute(query)
            tr = result.scalar_one_or_none()
            if tr:
                return None
            
            account.balance += amount
            new_tr = Transaction(unq_id=unq_id, account_id=account_id, amount=amount)
            session.add(new_tr)

            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return user


class AccountDAO(BaseDAO):
    model = Account

    @classmethod
    async def get_accounts(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(user_id=data_id)
            result = await session.execute(query)
            accs = result.scalar_one_or_none()
            return accs or [{'id': -1, 'balance': 0000}]


class TransactionDAO(BaseDAO):
    model = Transaction

    @classmethod
    async def get_transacts(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).select_from(Account).join(Account.transacts).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.all()

        