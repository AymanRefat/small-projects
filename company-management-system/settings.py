from sqlalchemy.orm import Session
from utils.funcs import sqlite_engine, mysql_engine
from os import getcwd

LOGGING = False

PATH = getcwd()

SQLITE_NAME = "db.sqlite"

TEST_DB_NAME = "testdb.sqlite"

DB_ENGINE = sqlite_engine(LOGGING, SQLITE_NAME)

EXIT_OPT = True

SESSION_MAKER = Session(DB_ENGINE)

KIND_OPTS = ["freelancer", "fulltime", "parttime"]
