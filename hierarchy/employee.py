from helpers.validate import validate_uuid


class Employee:
    """
    The Employee class that helps us model an employee and their supervisor, assign them a unique id, the id of the
    supervisor, it's left (lft) and right (rgt) values which indicate the position of the entry following the
    modified preorder traversal on the organization tree.
    This model helps us implement a nested sets model to store and easily access hierarchical data in a relational
    database
    """
    def __init__(self, name, supervisor=None):
        self.name = name
        self.supervisor = supervisor
        self._subordinates = []
        self.lft = 0
        self.rgt = 0
        self.employee_id = None
        self.supervisor_id = None

    @property
    def name(self):
        """
        Gets the name value
        :return: name (str)
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name property
        :param name (str): Should not be empty
        """
        if not isinstance(name, str):
            raise TypeError('name should be a string')
        if not name.strip():
            raise ValueError('name should not be an empty string')
        self._name = name.strip()

    @property
    def supervisor(self):
        """
        Gets the supervisor of this employee
        :return: supervisor (Employee)
        """
        return self._supervisor

    @supervisor.setter
    def supervisor(self, supervisor):
        """
        Sets the supervisor property of the employee
        :param supervisor: The supervisor of the current employee. Should be of type Employee or None
        """
        if supervisor and not isinstance(supervisor, Employee):
            raise TypeError('supervisor should be of type Employee')
        self._supervisor = supervisor

    @property
    def lft(self):
        """
        Gets the lft value
        :return: lft (int)
        """
        return self._lft

    @lft.setter
    def lft(self, lft):
        """
        Sets the lft property
        :param lft (int): The left pointer. Should be an integer
        """
        if not isinstance(lft, int):
            raise TypeError('lft should be an integer')
        self._lft = lft

    @property
    def rgt(self):
        """
        Gets the rgt value
        :return: rgt (int)
        """
        return self._rgt

    @rgt.setter
    def rgt(self, rgt):
        """
        Sets the rgt property
        :param rgt (int): The right pointer. Should be an integer
        """
        if not isinstance(rgt, int):
            raise TypeError('rgt should be an integer')
        self._rgt = rgt

    @property
    def employee_id(self):
        """
        Gets the employee_id value
        :return: employee_id (str)
        """
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        """
        Sets the employee_id property to a unique identifier used as a primary key in the database
        :param employee_id (str): Should be a UUID string or None
        """
        try:
            if validate_uuid(employee_id):
                self._employee_id = employee_id
            else:
                raise ValueError("Id is an invalid UUID string")
        except (ValueError, TypeError):
            raise

    @property
    def supervisor_id(self):
        """
        Gets the supervisor_id value
        :return: supervisor_id (str)
        """
        return self._supervisor_id

    @supervisor_id.setter
    def supervisor_id(self, supervisor_id):
        """
        Sets the supervisor_id property, which is the employee_id of the supervisor
        :param supervisor_id (str): Should be a UUID string or None
        """
        try:
            if validate_uuid(supervisor_id):
                self._supervisor_id = supervisor_id
            else:
                raise ValueError("Id is an invalid UUID string")
        except (ValueError, TypeError):
            raise

    @property
    def subordinates(self):
        """
        Gets the subordinates of this employee. These are employees which are supervised by the current employee
        :return: subordinates (List<Employee>)
        """
        return self._subordinates

    def add_subordinate(self, employee):
        """
        Add a employee who is directly supervised by the current employee
        :param employee: The employee to add. Should of type Employee
        """
        if not isinstance(employee, Employee):
            raise TypeError("employee to be added should be of type Employee")
        self._subordinates.append(employee)

    def __repr__(self):
        return f'Employee: (name: {self.name}, id: {self.employee_id})'
