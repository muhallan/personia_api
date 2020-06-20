from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from helpers.validate import check_json_contains_loop, validate_json


hierarchy_blueprint = Blueprint('hierarchy', __name__, url_prefix='/api/v1')


class StructureHierarchyView(MethodView):
    """
    View to structure the posted JSON into a well ordered employee hierarchy
    """
    def post(self):
        raw_data = request.get_data(as_text=True, parse_form_data=True)
        if not raw_data:
            response = {
                'status': 'fail',
                'message': 'No post body provided.'
            }
            return make_response(jsonify(response)), 400

        if not validate_json(raw_data):
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


# define the API resources
structure_view = StructureHierarchyView.as_view('structure_api')

# add Rules for API Endpoints
hierarchy_blueprint.add_url_rule(
    '/hierarchy/structure',
    view_func=structure_view,
    methods=['POST']
)
