from .model_mixin import app, db, ModelMixin


class Employee(ModelMixin):
    """
    The employee model. This represents the employee for the company, both the supervisor and the subordinate.
    It represents an adjacency model plus nested sets model, for storing hierarchical data
    """
    __tablename__ = 'employee'

    employee_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    supervisor_id = db.Column(db.String(64), db.ForeignKey('employee.employee_id'), nullable=True)
    lft = db.Column(db.Integer, default=0)
    rgt = db.Column(db.Integer, default=0)

    def __init__(self, employee_id, name, supervisor_id, lft, rgt):
        """
        Initialize the employee instance
        """
        self.employee_id = employee_id
        self.name = name
        self.supervisor_id = supervisor_id
        self.lft = lft
        self.rgt = rgt
