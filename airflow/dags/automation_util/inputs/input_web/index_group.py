from automation_util.inputs.dto import InputOutput
from automation_util.inputs.input_web.dto import TextMessageInput
from automation_util.inputs.input_web.task_text_message import get_output as task_text_get_output
from automation_util.inputs.input_web.task_text_message import (
    retrieve_text_message as task_retrieve_message,
)

from airflow.sdk import task_group

_BASE_GROUP_ID = "web-input"


@task_group(group_id=f"{_BASE_GROUP_ID}-text-input")
def text_input_group(text_input: TextMessageInput) -> InputOutput:
    message = task_retrieve_message(input_=text_input)
    output = task_text_get_output(message=message, text_input=text_input)
    return output


@task_group(group_id=f"{_BASE_GROUP_ID}")
def index_group(text_input: TextMessageInput) -> InputOutput:
    return text_input_group(text_input=text_input)
