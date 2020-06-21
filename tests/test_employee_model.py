import uuid
from tests.base_test import BaseTestCase
from models.employee import Employee


class TestEmployeeModel(BaseTestCase):

    def test_insert_employee(self):
        emp_id = uuid.uuid4().hex
        employee = Employee(
            employee_id=emp_id,
            name="Jack Hughes",
            supervisor_id=None,
            lft=1,
            rgt=2
        )
        result = employee.save()
        self.assertTrue(result)
        db_employee = Employee.get(emp_id)
        self.assertIsNotNone(db_employee)
        self.assertEqual(db_employee.employee_id, emp_id)
        self.assertEqual(db_employee.name, "Jack Hughes")

    def test_delete_all_employees(self):
        emp_id = uuid.uuid4().hex
        employee1 = Employee(
            employee_id=uuid.uuid4().hex,
            name="Jack Hughes",
            supervisor_id=None,
            lft=1,
            rgt=4
        )
        employee1.save()
        employee2 = Employee(
            employee_id=uuid.uuid4().hex,
            name="Ryan Reynolds",
            supervisor_id=emp_id,
            lft=2,
            rgt=4
        )
        employee2.save()
        inserted_employees = Employee.fetch_all()
        self.assertEqual(len(inserted_employees), 2)
        # delete all the employees
        result = Employee.delete_all_records()
        self.assertTrue(result)
        current_employees = Employee.fetch_all()
        self.assertEqual(len(current_employees), 0)
