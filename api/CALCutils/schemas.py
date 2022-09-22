import marshmallow as ma


class GetAgeQSchema(ma.Schema):
    date_of_birth = ma.fields.String(
        required=True, description="Date of birth", example="1992-04-23"
    )
    at_date = ma.fields.String(
        required=False,
        description="Date at which you would like the age to be calculated",
        example="2022-04-23",
    )


class GetAgeRSchema(ma.Schema):
    age = ma.fields.Float(default=30)
