from typing import List

from pydantic import BaseModel, Field


class ValidationMessage(BaseModel):
    message: str
    location: str


class RegistrationResponse(BaseModel):
    status: str
    validation_messages: List[ValidationMessage] = Field(default=list(), alias="validationMessages")
