import requests
from airflow_config import get_settings
from automation_util.inputs.input_web.dto import TextMessageInput
from automation_util.perform_actions.note.dto import Note

from airflow.sdk import task


def get_note_url(user_id: int, thread_id: int) -> str:
    base_api_url = get_settings().application_backend.url
    return f"{base_api_url}/notes/user/{user_id}/thread/{thread_id}"


@task
def process_note_to_api(
    text_input: TextMessageInput,
    note: Note,
):
    url = get_note_url(
        user_id=text_input.user_id,
        thread_id=text_input.thread_id,
    )
    token = get_settings().application_backend.token
    data = {
        "title": note.title,
        "content": note.content or "",
    }
    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {token}",
        },
        json=data,
    )
    response.raise_for_status()
