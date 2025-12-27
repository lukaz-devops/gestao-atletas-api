from typing import Annotated
from pydantic import UUID4, BaseModel, ConfigDict, Field
from datetime import datetime


class BaseSchema(BaseModel):
        model_config = ConfigDict(
            from_attributes = True,
            arbitrary_types_allowed=True,
            extra='forbid'
        )


class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]