import traceback

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from CALCcomp import utils as CALCcomp_utils

from api.logger import logger
from api.CALCutils.schemas import GetAgeQSchema, GetAgeRSchema
from api.CALCutils.urls import API_UTILS_GET_AGE
from api.urls import API_UTILS

blp = Blueprint(
    name="Utils",
    import_name="utils",
    url_prefix=API_UTILS,
    description="Utility functions",
)


@blp.route(API_UTILS_GET_AGE)
class GetAgeView(MethodView):
    @blp.arguments(GetAgeQSchema, location="json")
    @blp.response(200, GetAgeRSchema(many=False))
    def post(self, data):
        """Calculate the age

        Get age from date_of_birth, you can pass a date in which you would like age to be calculated.
        """
        try:
            req_data = GetAgeQSchema.from_dict(data)
            if hasattr(req_data, "at_date"):
                age = CALCcomp_utils.get_age(req_data.date_of_birth, req_data.at_date or None)
            else:
                age = CALCcomp_utils.get_age(req_data.date_of_birth)
            return GetAgeRSchema.from_dict({"age": age})
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())
            abort(500, message=e.__class__.__name__, errors=str(e))
