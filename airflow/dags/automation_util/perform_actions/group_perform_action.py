from automation_util.classification.dto import Action
from automation_util.inputs.dto import InputOutput
from automation_util.inputs.input_web.dto import TextMessageInput
from automation_util.perform_actions.note.task_extract_note import extract_note_from_input
from automation_util.perform_actions.note.task_process_note_to_api import process_note_to_api
from automation_util.perform_actions.task.task_extract_task import extract_task_from_input
from automation_util.perform_actions.task.task_process_task_to_api import process_task_to_api

from airflow.sdk import task, task_group

_BASE_GROUP_ID = "perform-action"


@task_group(group_id=f"{_BASE_GROUP_ID}-note-flow")
def perform_note_flow(input_: InputOutput, text_input: TextMessageInput):
    note = extract_note_from_input(input_=input_)
    process_note_to_api(note=note, text_input=text_input)


@task_group(group_id=f"{_BASE_GROUP_ID}-task-flow")
def perform_task_flow(input_: InputOutput, text_input: TextMessageInput):
    task_ = extract_task_from_input(input_=input_)
    process_task_to_api(actionable_task=task_, text_input=text_input)


@task.branch
def branch_logic(action: Action):
    prefix = f"{_BASE_GROUP_ID}"

    if action.type == "note":
        return f"{prefix}.{prefix}-note-flow"

    elif action.type == "task":
        return f"{prefix}.{prefix}-task-flow"
    else:
        raise ValueError(f"Unknown action type: {action.type}")


@task_group(group_id=f"{_BASE_GROUP_ID}")
def perform_action(action: Action, input_: InputOutput, text_input: TextMessageInput):
    decision = branch_logic(action=action)

    note_flow = perform_note_flow(input_=input_, text_input=text_input)
    task_flow = perform_task_flow(input_=input_, text_input=text_input)

    decision >> [note_flow, task_flow]
