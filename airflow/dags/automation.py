from datetime import datetime

from automation_util.classification.task_input_classification import perform_classification
from automation_util.inputs.input_web.index_group import index_group as input_web_group
from automation_util.inputs.input_web.task_input_parser import parse_input as task_parse_input
from automation_util.perform_actions.group_perform_action import perform_action

from airflow.sdk import dag

DEFAULT_PAYLOAD = {
    "user_id": 2,
    "thread_id": 1,
    "thread_message_id": 1,
}


@dag(
    dag_id="automation",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["dispatcher"],
    params={"payload": DEFAULT_PAYLOAD},
)
def task_dispatcher():
    text_input = task_parse_input()
    input_ = input_web_group(text_input)
    action = perform_classification(input_=input_)
    perform_action(action=action, input_=input_, text_input=text_input)


task_dispatcher()
