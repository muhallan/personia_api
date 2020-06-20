import unittest
import uuid
from hierarchy.employee import Employee


class TestEmployeeClass(unittest.TestCase):

    def test_employee_class_instantiates(self):
        employee = Employee("my name")
        self.assertIsInstance(employee, Employee)

    def test_employee_name(self):
        employee1 = Employee("John Doe")
        self.assertEqual(employee1.name, "John Doe")
        employee2 = Employee(" Peter Miles ")
        self.assertEqual(employee2.name, "Peter Miles")
        with self.assertRaisesRegex(ValueError, 'name should not be an empty string'):
            Employee("")
        with self.assertRaisesRegex(TypeError, 'name should be a string'):
            Employee(435)

    def test_employee_supervisor(self):
        employee = Employee("Test User")
        self.assertIsNone(employee.supervisor)
        manager = Employee("Joe Briggs")
        employee.supervisor = manager
        self.assertEqual(employee.supervisor, manager)
        with self.assertRaisesRegex(TypeError, 'supervisor should be of type Employee'):
            Employee("Person X", "Hannah Montana")

    def test_employee_lft(self):
        employee = Employee("Human")
        employee.lft = 3
        self.assertEqual(employee.lft, 3)
        with self.assertRaisesRegex(TypeError, 'lft should be an integer'):
            employee = Employee("R.J Brud")
            employee.lft = "2"

    def test_employee_rgt(self):
        employee = Employee("Human Z")
        employee.rgt = 1
        self.assertEqual(employee.rgt, 1)
        with self.assertRaisesRegex(TypeError, 'rgt should be an integer'):
            employee = Employee("F. Brudy")
            employee.rgt = "9"

    def test_employee_id(self):
        employee = Employee("Grace Hopper")
        self.assertIsNone(employee.employee_id)
        emp_id = uuid.uuid4().hex
        employee.employee_id = emp_id
        self.assertEqual(employee.employee_id, emp_id)
        with self.assertRaisesRegex(TypeError, 'Id should be of type string'):
            employee.employee_id = 45678942
        with self.assertRaisesRegex(ValueError, 'Id is not a valid UUID'):
            employee.employee_id = "6789g6dgh7832d"
        with self.assertRaisesRegex(ValueError, 'Id should not be empty'):
            employee.employee_id = ""

    def test_employee_supervisor_id(self):
        employee = Employee("Classy Martins")
        self.assertIsNone(employee.supervisor_id)
        sup_id = uuid.uuid4().hex
        employee.supervisor_id = sup_id
        self.assertEqual(employee.supervisor_id, sup_id)
        with self.assertRaisesRegex(TypeError, 'Id should be of type string'):
            employee.supervisor_id = 76893
        with self.assertRaisesRegex(ValueError, 'Id is not a valid UUID'):
            employee.supervisor_id = "ttwwnd82"
        with self.assertRaisesRegex(ValueError, 'Id should not be empty'):
            employee.supervisor_id = ""

    def test_employee_add_subordinate(self):
        employee = Employee("Billy Joe")
        self.assertListEqual(employee.subordinates, [])
        subordinate = Employee("Freddy Kruger")
        employee.add_subordinate(subordinate)
        self.assertListEqual(employee.subordinates, [subordinate])
        with self.assertRaisesRegex(TypeError, 'employee to be added should be of type Employee'):
            employee.add_subordinate("Employee name")
