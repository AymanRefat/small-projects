import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session


def combine_dicts(*dicts: dict) -> dict:
    """Combine Dicts in one Dict"""
    if len(dicts) == 0:
        return {}
    if len(dicts) == 1:
        return dicts[0]
    return {**dicts[0], **combine_dicts(*dicts[1:])}


def mysql_engine(logging: bool) -> Engine:
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")
    connection_string = (
        f"mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}"
    )

    return create_engine(connection_string, echo=logging)


def sqlite_engine(logging: bool, name) -> Engine:
    return create_engine(f"sqlite:///{name}", echo=logging)


def get_test_sqlite_engine(logging: bool, name: str) -> Engine:
    return create_engine(f"sqlite:///{name}", echo=logging)


def get_test_session_maker(engine: Engine) -> Session:
    return Session(engine)
