from automation_util.inputs.input_web.dto import TextMessageInput

from airflow.sdk import task


@task
def parse_input(**context) -> TextMessageInput:
    params = context.get("params", {})
    payload = params.get("payload", {})

    thread_id = int(payload.get("thread_id"))
    thread_message_id = int(payload.get("thread_message_id"))
    user_id = int(payload.get("user_id"))

    return TextMessageInput(
        thread_id=thread_id,
        thread_message_id=thread_message_id,
        user_id=user_id,
    )
