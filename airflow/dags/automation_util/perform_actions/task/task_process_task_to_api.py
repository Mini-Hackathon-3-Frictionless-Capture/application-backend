import requests
from airflow_config import get_settings
from automation_util.inputs.input_web.dto import TextMessageInput
from automation_util.perform_actions.task.dto import ActionableTask

from airflow.sdk import task


def get_task_url(user_id: int, thread_id: int) -> str:
    base_api_url = get_settings().application_backend.url
    return f"{base_api_url}/tasks/user/{user_id}/thread/{thread_id}"


@task
def process_task_to_api(
    text_input: TextMessageInput,
    actionable_task: ActionableTask,
):
    url = get_task_url(
        user_id=text_input.user_id,
        thread_id=text_input.thread_id,
    )
    token = get_settings().application_backend.token
    meta_data = {"due_date": actionable_task.due_date} if actionable_task.due_date else {}
    data = {
        "title": actionable_task.title,
        "content": actionable_task.content or "",
        "meta_data": meta_data,
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
