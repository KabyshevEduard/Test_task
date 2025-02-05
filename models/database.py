from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from dotenv import load_dotenv
import os


HOST = os.getenv('PG_HOST')
engine = create_async_engine(url=HOST)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)
