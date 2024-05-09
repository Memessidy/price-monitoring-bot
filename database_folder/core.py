from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

load_dotenv(find_dotenv())

sync_engine = create_engine(url=f"sqlite:///{os.getenv('DATABASE_PATH')}")
sync_session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
