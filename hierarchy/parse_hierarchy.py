import uuid
from collections import defaultdict
from hierarchy.employee import Employee


def organize_hierarchy(hierarchy_dict):
    """
    Creates a dictionary with the hierarchy from the top boss (CEO) to the subordinates who don't have
    people they supervise
    :param hierarchy_dict: dict. The dictionary to organize
    :return: organized hierarchy dict: dict
    """
    top_down_hierarchy = defaultdict(dict)
    for employee, supervisor in hierarchy_dict.items():
        manager = top_down_hierarchy[supervisor]
        manager[employee] = top_down_hierarchy[employee]

        # remove the previously created employee key since it has now been assigned to a manager
        top_down_hierarchy.pop(employee)

    return dict(top_down_hierarchy)


def construct_hierarchy_tree(top_down_hierarchy_dict):
    """
    Constructs a tree consisting of Employee nodes with the root being the top most supervisor and the leaves are
    the employees who are just subordinates (not supervisors)
    :param top_down_hierarchy_dict: organized dictionary to parse into a tree
    :return: root of the Employee n-ary tree: Employee
    """
    if not top_down_hierarchy_dict:
        return None

    all_employees = {}

    # do a breadth first search (BFS) on the hierarchy using a queue
    # the queue contains the employees' names initialized to the top most employee
    queue = [next(iter(top_down_hierarchy_dict))]

    # the top most supervisor
    root_employee = None

    while queue:
        employee_name = queue.pop(0)
        if employee_name not in all_employees:
            # this is for the root supervisor (E.g. CEO)
            supervisor_employee = Employee(name=employee_name)
            root_employee = supervisor_employee
            all_employees[employee_name] = supervisor_employee
        else:
            supervisor_employee = all_employees[employee_name]

        if employee_name not in top_down_hierarchy_dict:
            # we have reached the end of this branch
            continue
        else:
            # get the new top_down_hierarchy_dict with the current employee as the top most
            top_down_hierarchy_dict = top_down_hierarchy_dict[employee_name]

            for subordinate_name in top_down_hierarchy_dict:
                subordinate_employee = Employee(name=subordinate_name, supervisor=supervisor_employee)
                supervisor_employee.add_subordinate(subordinate_employee)
                all_employees[subordinate_name] = subordinate_employee
                queue.append(subordinate_name)
    return root_employee


def do_mptt_traversal(organized_hierarchy_dict):
    """
    Create a dictionary to store the modified preorder tree traversal (mptt) tree employee values for insertion in the
    database. This calculates the lft and rgt values for each node, for use in the nested sets model, and sets a
    supervisor_id for each employee. This makes a hybrid of adjacency model and nested sets model

    Sample item in the mptt dict:
    {
        "Sophie": {
            "name": "Sophie",
            "lft": 2,
            "rgt": 9,
            "id": "ef68absfg3342",
            "supervisor_id": "257cde2534325"
        }
    }
    :param organized_hierarchy_dict: organized dictionary to parse into a tree
    :return: dictionary with employees and their respective values for the Employee database model: dict
    """

    mptt_dict = {}
    root = construct_hierarchy_tree(organized_hierarchy_dict)
    stack = []
    if not root:
        return mptt_dict

    stack.append(root)

    counter = 0

    while stack:
        employee = stack[-1]
        supervisor = employee.supervisor
        if not supervisor:
            # this is a root
            supervisor_id = None
        else:
            supervisor_id = mptt_dict[supervisor.name]['id']

        employee_id = uuid.uuid4().hex
        if employee.name not in mptt_dict:
            # we are seeing this employee for the first time, so we set their "lft" value. The "rgt" will just be the
            # initial '0'.
            counter += 1
            employee.lft = counter
            mptt_dict[employee.name] = {
                'name': employee.name,
                "id": employee_id,
                "supervisor_id": supervisor_id,
                "lft": employee.lft,
                "rgt": employee.rgt
            }

            # reverse the children so that when added to the stack, the starting child is picked first
            subordinates = reversed(employee.subordinates)
            for subordinate in subordinates:
                stack.append(subordinate)
        else:
            # we are now seeing this employee for the second time, so we set the "rgt" value.
            counter += 1
            mptt_dict[employee.name]['rgt'] = counter
            # we are done with it, remove it from the stack
            stack.pop()

    return mptt_dict
