import marshmallow as ma
from CALCcomp.models import Human, CalcSession, CalcTestInput
from CALCcomp.parameters import ETHNICITY_ALLOWED, SEX_ALLOWED, TEST_TYPE_ALLOWED

from api.CALCcalc.enumfield import EnumField


class HumanSchema(ma.Schema):
    """Human model schema"""

    age = ma.fields.Float(description="Age", allow_none=True)
    sex = EnumField(choices=SEX_ALLOWED, name="Sex", required=True)
    height_in_cm = ma.fields.Float(description="Height in cm", example=187.3)
    ethnicity = EnumField(choices=ETHNICITY_ALLOWED, name="Ethnicity", required=True)
    weight_in_kg = ma.fields.Float(description="Weight in kg", example=87.5, allow_none=True)

    @ma.post_load
    def make_human(self, data, **kwargs) -> Human:
        try:
            return Human(**data)
        except Exception as e:
            print(data, str(e))
            raise ma.ValidationError(str(e))


class TestOverwriteSchema(ma.Schema):
    """Feedback included in the test from the operator"""

    fvc_status = EnumField(choices=["acceptable", "usable", "unusable", "unknown"], name="FVC Status", required=False)
    fvc_comment = ma.fields.String(description="FVC comment for the test", default="")
    fev1_status = EnumField(choices=["acceptable", "usable", "unusable", "unknown"], name="FEV1 Status", required=False)
    fev1_comment = ma.fields.String(description="FEV1 feedback for the test", default="")
    is_best = ma.fields.Boolean(description="If this test is the best one of the session", default=False)


class TestSchema(ma.Schema):
    """Test model schema"""

    id = ma.fields.String(description="UUID")
    forced_exhale_flow_array = ma.fields.List(
        ma.fields.Float,
        description="Forced exhale array. This is where most of observables come from.",
    )
    forced_inhale_flow_array = ma.fields.List(
        ma.fields.Float,
        description="Forced inhale array. Second part of the full loop (after forced_exhale_flow_array).",
    )
    deep_inhale_flow_array = ma.fields.List(
        ma.fields.Float,
        description="Deep inhale array. This is the inhale you do before the forced full loop.",
    )
    fvc_measured_device = ma.fields.Float(
        description="Calculated by Calcmeter. Some values need to come from Calcmeter directly, for compliance.",
        default=0,
        allow_none=True,
    )

    fev1_measured_device = ma.fields.Float(description="TBD", default=0, allow_none=True)
    pef_measured_device = ma.fields.Float(description="TBD", default=0, allow_none=True)
    fivc_measured_device = ma.fields.Float(description="TBD", default=0, allow_none=True)
    fiv1_measured_device = ma.fields.Float(description="TBD", default=0, allow_none=True)
    pif_measured_device = ma.fields.Float(description="TBD", default=0, allow_none=True)

    overwrite = ma.fields.Nested(TestOverwriteSchema, allow_none=True)

    @ma.post_load
    def make_test(self, data, **kwargs) -> CalcTestInput:
        try:
            return CalcTestInput(**data)
        except Exception as e:
            print(data, str(e))
            raise ma.ValidationError(str(e))


class AnalysisQSchema(ma.Schema):
    session_type = EnumField(choices=TEST_TYPE_ALLOWED, name="Session type", required=True)
    sampling_size = ma.fields.Float(description="Sampling size", default=0.01)
    human = ma.fields.Nested(HumanSchema, rquired=True)
    tests = ma.fields.List(ma.fields.Nested(TestSchema), description="All tests for a session", required=True)

    @ma.post_load
    def make_session(self, data, **kwargs) -> CalcSession:
        try:
            return CalcSession(**data)
        except Exception as e:
            raise ma.ValidationError(str(e))
