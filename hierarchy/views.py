import logging
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from hierarchy.parse_hierarchy import do_mptt_traversal, organize_hierarchy
from helpers.validate import check_json_contains_loop, validate_json
from auth.decorator import authorization
from models.employee import Employee
from models.model_mixin import db


hierarchy_blueprint = Blueprint('hierarchy', __name__, url_prefix='/api/v1')


class StructureHierarchyView(MethodView):
    """
    View to structure the posted JSON into a well ordered employee hierarchy
    """
    @authorization
    def post(self, *args, **kwargs):
        # get the logged in user_id from the authorization kwargs for use when needed
        user_id = kwargs['user_id']

        # get the raw post data
        raw_data = request.get_data(as_text=True, parse_form_data=True)
        if not raw_data:
            response = {
                'status': 'fail',
                'message': 'No post body provided.'
            }
            return make_response(jsonify(response)), 400

        hierarchy_dict = validate_json(raw_data)
        if not hierarchy_dict:
            response = {
                'status': 'fail',
                'message': 'Invalid JSON posted. Please check the format.'
            }
            return make_response(jsonify(response)), 400

        duplicate_keys = check_json_contains_loop(raw_data)
        if duplicate_keys:
            response = {
                'status': 'fail',
                'message': f'The posted JSON contains loops. '
                f'These employees have more than one supervisor: {duplicate_keys}'
            }
            return make_response(jsonify(response)), 400

        organized_hierarchy = organize_hierarchy(hierarchy_dict)
        if len(organized_hierarchy) > 1:
            # this means that there multiple roots in the hierarchy
            roots = list(organized_hierarchy.keys())
            response = {
                'status': 'fail',
                'message': f'There are multiple roots in the hierarchy: {roots}'
            }
            return make_response(jsonify(response)), 400

        # first empty the Employee table since we are doing a replace
        result = Employee.delete_all_records()
        if not result:
            logging.error(f"An error has occurred while deleting employee records")
            response = {
                'status': 'fail',
                'message': 'Failed to delete employees already in the database'
            }
            return make_response(jsonify(response)), 500

        # insert the employees into the employee table in the database
        mptt_employees_dict = do_mptt_traversal(organized_hierarchy)
        try:
            for employee_dict in mptt_employees_dict.values():
                employee = Employee(
                    employee_id=employee_dict['id'],
                    name=employee_dict['name'],
                    supervisor_id=employee_dict['supervisor_id'],
                    lft=employee_dict['lft'],
                    rgt=employee_dict['rgt']
                )
                # save the employee in the database
                db.session.add(employee)
            # commit the changes
            db.session.commit()
        except Exception as e:
            logging.error(f"An error has occurred while inserting an employee - {e}")
            response = {
                'status': 'fail',
                'message': 'Saving the employees hierarchy failed.'
            }
            return make_response(jsonify(response)), 500
        response = {
            "status": "success",
            "employee_hierarchy": organized_hierarchy
        }
        return make_response(jsonify(response)), 201


# define the API resources
structure_view = StructureHierarchyView.as_view('structure_api')

# add Rules for API Endpoints
hierarchy_blueprint.add_url_rule(
    '/hierarchy/structure',
    view_func=structure_view,
    methods=['POST']
)
