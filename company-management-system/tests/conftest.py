import pytest
from sqlalchemy.orm import Session
import os
from datetime import date
import random as rd

from settings import PATH, TEST_DB_NAME
from models.employee import Employee, WorkedHours
from utils.option import Option
from utils.signal import Signal
from utils.funcs import get_test_session_maker, get_test_sqlite_engine
from models.base import Base


def create_employee(SessionMaker: Session, d: dict) -> Employee:
    with SessionMaker as session:
        obj = Employee(**d)
        session.add(obj)
        session.commit()
        return session.query(Employee).filter(Employee.name == d.get("name")).first()


class OptExcute(Option):
    def excute(self) -> Signal:
        pass

    def task(self) -> str:
        pass


class OptRaiseErr(Option):
    def excute(self) -> Signal:
        raise Exception()

    def task(self) -> str:
        pass


@pytest.fixture(scope="session")
def opt_excute():
    opt = OptExcute(False)
    return opt


@pytest.fixture(scope="session")
def opt_raise_err():
    opt = OptRaiseErr(False)
    return opt


@pytest.fixture(scope="session")
def employee_dict1():
    return {
        "name": "SomeOnea",
        "job_title": "SomeJoba",
        "gender": "m",
        "kind": "freelancer",
    }


@pytest.fixture(scope="session")
def employee_dict2():
    return {
        "name": "SomeOneb",
        "job_title": "SomeJobb",
        "gender": "f",
        "kind": "fulltime",
    }


@pytest.fixture(scope="session")
def employee():
    return Employee(name="Someone", job_title="somejob", gender="m", kind="freelancer")


@pytest.fixture(scope="session")
def today():
    return date.today()


@pytest.fixture(scope="function")
def random_list_numbers():
    le = rd.randint(0, 100)
    l = []
    for _ in range(le):
        l.append(rd.randint(0, 100))
    return l


@pytest.fixture(scope="function", autouse=False)
def debug_database_rows():
    engine = get_test_sqlite_engine(True, TEST_DB_NAME)
    SessionMaker = get_test_session_maker(engine)
    print("+" * 10)
    with SessionMaker as session:
        q = session.query(Employee).all()
        for x in q:
            print(x)
        q2 = session.query(WorkedHours).all()
        for x in q2:
            print(q2)

    print("+" * 10)


@pytest.fixture(scope="class", autouse=True)
def SessionMaker(employee_dict2, employee_dict1):
    # Setup
    # Creating the Database and tables
    engine = get_test_sqlite_engine(False, TEST_DB_NAME)
    SessionMaker = get_test_session_maker(engine)
    Base._set_sessionmaker(SessionMaker)
    Base.create_tabels(engine)

    #  Create 2 Employees and 2 Worked Hours
    em1 = create_employee(SessionMaker, employee_dict1)
    em2 = create_employee(SessionMaker, employee_dict2)
    print("2 Employees Created")
    with SessionMaker as session:
        wh1 = WorkedHours(
            employee_id=em1.id,
            hours=5,
            hour_rate=9,
            worked_date=date.today(),
        )
        wh2 = WorkedHours(
            employee_id=em2.id,
            hours=7,
            hour_rate=9,
            worked_date=date.today(),
        )
        session.add(wh1, wh2)
        session.commit()

    yield SessionMaker
    # TearDown
    #  Deleting the Database
    os.remove(PATH + f"/{TEST_DB_NAME}")
