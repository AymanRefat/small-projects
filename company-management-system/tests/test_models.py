import pytest
from datetime import date
from models.employee import Employee, WorkedHours
from sqlalchemy.orm import Session
from tests.conftest import create_employee


def test_create_employee_wrong_gender():
    with pytest.raises(ValueError) as e:
        em = Employee(
            name="s",
            job_title="s",
            gender="wrong",
            kind="freelancer",
        )


def test_create_employee_wrong_kind():
    with pytest.raises(ValueError) as e:
        em = Employee(name="s", job_title="s", gender="m", kind="wrong")


def test_setting_gender_lower_case():
    em = Employee(
        name="someone",
        job_title="somejob",
        gender="M",
        kind="freelancer",
    )
    assert em.gender == "m"


def test_creating_worked_string_hours_and_rates(employee, today):
    with pytest.raises(TypeError) as e:
        wh = WorkedHours(
            employee_id=employee.id,
            hours="som",
            hour_rate="som",
            worked_date=today,
        )


def test_creating_worked_right_hours_and_rates(employee, today):
    wh = WorkedHours(
        employee_id=employee.id,
        hours=19,
        hour_rate=10,
        worked_date=today,
    )
    assert isinstance(wh.hour_rate, float)
    assert isinstance(wh.hours, float)


def test_creating_workedhours_date(employee, today):
    with pytest.raises(TypeError) as e:
        wh = WorkedHours(
            employee_id=employee.id,
            hours=19,
            hour_rate=10,
            worked_date=134,
        )


def test_creating_workedhours_date_righttype(employee, today):
    wh = WorkedHours(
        employee_id=employee.id,
        hours=19,
        hour_rate=10,
        worked_date=today,
    )
    assert isinstance(wh.worked_date, date)


def test_total_hours(
    employee_dict1, today, SessionMaker: Session, random_list_numbers: list
):
    hours = random_list_numbers

    employee = create_employee(SessionMaker, employee_dict1)

    with SessionMaker as session:
        for x in hours:
            wh = WorkedHours(
                employee_id=employee.id,
                hours=x,
                hour_rate=10,
                worked_date=today,
            )
            session.add(wh)
            session.commit()

        total = 0
        q = session.query(WorkedHours).filter(WorkedHours.employee_id == employee.id)
        for x in q:
            total += x.hours

    with SessionMaker as session:
        obj = session.query(Employee).filter(Employee.id == employee.id).first()
        assert obj.get_total_hours() == total
