from typing import List

from marshmallow.fields import String


class EnumField(String):
    """Custom field to represent enum"""

    def __init__(self, choices: List[str], name: str = "", **args):
        super().__init__(
            validate=lambda x: x in choices,
            description=f"{name} - one of {choices}",
            example=choices[0],
            **args,
        )
