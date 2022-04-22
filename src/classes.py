from fastapi import Query
from pydantic import BaseModel


class InputText(BaseModel):
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

    class Config:
        schema_extra = {
            "example": {
                "id": "1234_any_text",
                "text": "I travelled to California and met the Governor"
            }
        }
