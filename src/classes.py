# Place here your user defined classes

from fastapi import Query
from pydantic import BaseModel


# Input Text
class InputText(BaseModel):
    # Input must be at least one word of len=1
    id: str = Query(
        ...,
        min_length=1,
        description="This is the identifier label"
    )
    text: str = Query(
        ...,
        min_length=1,
        description="This is the text where to extract entities from"
    )

    # The following code helps to "build" a quick example
    # for the docs / redoc documentation, IT DOES NOT DO
    # ANYTHING (!)
    class Config:
        schema_extra = {
            "example": {
                "id": "1_of_many",
                "text": "Paris is the capital city of France"
            }
        }
