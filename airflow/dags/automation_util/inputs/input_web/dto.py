from typing import Literal

from pydantic import BaseModel


class TextMessageInput(BaseModel):
    user_id: int
    thread_id: int
    thread_message_id: int


class MessageResponse(BaseModel):
    id: int
    timestamp: str
    content: str
    is_bot_message: bool
    message_type: Literal["text", "voice", "image"]
    is_initial_thread_message: bool
    thread: int
    author: int | None
