from typing import Literal

from pydantic import BaseModel


class WebReference(BaseModel):
    url: str


class InputOutput(BaseModel):
    stream: Literal["telegram", "application"]
    type: Literal["text", "voice", "image"]
    reference: WebReference
    transcript: str
