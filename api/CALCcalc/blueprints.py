import json
import traceback

from flask import Response
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from api.logger import logger
from api.CALCcalc.schemas import AnalysisQSchema
from api.CALCcalc.urls import API_ANALYSIS_CALCULATE
from api.urls import API_ANALYSIS

blp = Blueprint(
    name="Calculation",
    import_name="calculation",
    url_prefix=API_ANALYSIS,
    description="Calculation functions",
)


@blp.route(API_ANALYSIS_CALCULATE)
class AnalysisView(MethodView):
    @blp.arguments(AnalysisQSchema, location="json")
    @blp.response(200, description="Analysis result in JSON")
    def post(self, data):
        """Calculate the CALC analysis for a session

        Wrapper of compute_session_summary_protocol_2019
        """
        try:
            # Calc_session = AnalysisQSchema.from_dict(data)
            Calc_session = data
            session_calculated_protocol_2019 = Calc_session.compute_session_summary_protocol_2019()
            return Response(response=json.dumps(session_calculated_protocol_2019), mimetype="application/json", status=200)
        except Exception as e:
            logger.error(str(e))
            logger.error(traceback.format_exc())

            abort(500, message=e.__class__.__name__, errors=str(e))
