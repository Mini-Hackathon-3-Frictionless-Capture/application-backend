import requests
from airflow_config import get_settings
from automation_util.inputs.dto import InputOutput, WebReference
from automation_util.inputs.input_web.dto import MessageResponse, TextMessageInput

from airflow.sdk import task


def get_thread_url(user_id: int, thread_id: int, thread_message_id: int) -> str:
    base_api_url = get_settings().application_backend.url
    return f"{base_api_url}/threads/user/{user_id}/thread/{thread_id}/message/{thread_message_id}"


@task
def retrieve_text_message(input_: TextMessageInput) -> MessageResponse:
    url = get_thread_url(
        user_id=input_.user_id,
        thread_id=input_.thread_id,
        thread_message_id=input_.thread_message_id,
    )

    token = get_settings().application_backend.token
    response = requests.get(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {token}",
        },
    )
    response.raise_for_status()
    return MessageResponse(**response.json())


@task
def get_output(message: MessageResponse, text_input: TextMessageInput) -> InputOutput:
    url = get_thread_url(
        user_id=text_input.user_id,
        thread_id=message.thread,
        thread_message_id=message.id,
    )
    return InputOutput(
        stream="application",
        type="text",
        reference=WebReference(url=url),
        transcript=message.content,
    )
