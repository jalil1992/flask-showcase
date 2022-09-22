import json
import os

from api.CALCcalc.schemas import AnalysisQSchema
from api.CALCcalc.urls import API_ANALYSIS_CALCULATE
from api.tests.sample_flow_arrays import flow_array_no_errors
from api.urls import API_ANALYSIS
from CALCcomp.models import CalcSession, CalcTestInput, Human
from CALCcomp.parameters import TEST_TYPE_FULL_LOOP


def test_Calc_session_protocol_2019(client):
    # load test data from CALCcomp
    human = Human(age=18.2, height_in_cm=160, sex="female", ethnicity="ethnicity_south_east_asian")

    flow_array_no_errors_inhale = [-k for k in flow_array_no_errors]

    ###############
    # TEST 1
    ###############
    # CALCcomp
    tests = [
        CalcTestInput(
            id="83ef7783-1264-4c83-a875-ff7a77ae043b",
            forced_exhale_flow_array=flow_array_no_errors,
            forced_inhale_flow_array=[1.05 * k for k in flow_array_no_errors_inhale],
            deep_inhale_flow_array=flow_array_no_errors_inhale,
        ),
        CalcTestInput(
            id="83ef7783-1264-4c83-a875-a63877ae043b",
            forced_exhale_flow_array=[0.95 * k for k in flow_array_no_errors],
            forced_inhale_flow_array=flow_array_no_errors_inhale,
            deep_inhale_flow_array=flow_array_no_errors_inhale,
        ),
    ]
    session = CalcSession(human=human, tests=tests, session_type=TEST_TYPE_FULL_LOOP, sampling_size=0.01)

    session1_results = session.compute_session_summary_protocol_2019()

    # build test data in json and save for test on postman
    session_1_dump = AnalysisQSchema().dump(session)

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, "test_session_1.json"), "w") as file:
        file.write(json.dumps(session_1_dump))

    # api response
    response_1 = client.post(API_ANALYSIS + API_ANALYSIS_CALCULATE, json=session_1_dump)

    # validation
    assert response_1.status_code == 200
    assert response_1.data.decode("utf-8") == json.dumps(session1_results)
