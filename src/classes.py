# Place here your user defined classes
# I will modify now this comment, and test a commit

from fastapi import Query
from pydantic import BaseModel


# Input Text
class InputText(BaseModel):
    # Input must be at least one word of len=1
    id: str = Query(
        ...,
        min_length=1,
        description="Identifier label"
    )
    text: str = Query(
        ...,
        min_length=1,
        description="Where to extract entities from"
    )

    # The following code helps to "build" a quick example
    # for the docs / redoc documentation, IT DOES NOT DO
    # ANYTHING (!)
    class Config:
        schema_extra = {
            "example": {
                "id": "any_string_identifier_of_your_choice",
                "text": "Python and C++ are important programming languages"
            }
        }
