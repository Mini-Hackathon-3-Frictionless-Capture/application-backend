from airflow_config import get_settings
from automation_util.inputs.dto import InputOutput
from automation_util.perform_actions.task.dto import ActionableTask
from llm.llm_templates import LLMExtractTask
from llm.repository import Message, OpenAIModel
from openai.types.chat import ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition

from airflow.sdk import task


@task
def extract_task_from_input(
    input_: InputOutput,
) -> ActionableTask:
    llm = LLMExtractTask(config=get_settings().open_ai)
    identity_message = Message(
        role="system",
        content=llm.get_identity_prompt(language_code="de"),
    )
    action_message = Message(
        role="system",
        content=llm.get_action_prompt(language_code="de"),
    )
    user_message = Message(
        role="user",
        content=input_.transcript,
    )
    parameters_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": (
                    "Ein handlungsorientierter Titel, der mit einem VERB beginnt (Imperativ). "
                    "Muss ohne weiteren Kontext verständlich sein."
                ),
            },
            "content": {
                "type": "string",
                "description": (
                    "Details, Unteraufgaben (Checklisten) oder Kontext. LEER LASSEN (null), "
                    "wenn der Titel bereits alles sagt."
                ),
            },
            "due_date": {
                "type": "string",
                "description": (
                    "Das Fälligkeitsdatum im Format YYYY-MM-DD. Nur ausfüllen, wenn im Text ein "
                    "expliziter Zeitpunkt genannt wird (z.B. 'bis Freitag', 'morgen')."
                ),
            },
        },
        "required": ["title"],
    }
    tools = ChatCompletionFunctionToolParam(
        type="function",
        function=FunctionDefinition(
            name="create_actionable_task",
            description=(
                "Transforms raw input into a single actionable task with optional deadline."
            ),
            parameters=parameters_schema,
        ),
    )
    reply = llm.perform_tool_prompt(
        model=OpenAIModel.gpt_5,
        messages=[identity_message, action_message, user_message],
        tools=[tools],
        output_type=ActionableTask,
    )
    return reply
