from airflow_config import get_settings
from automation_util.inputs.dto import InputOutput
from automation_util.perform_actions.note.dto import Note
from llm.llm_templates import LLMExtractNote
from llm.repository import Message, OpenAIModel
from openai.types.chat import ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition

from airflow.sdk import task


@task
def extract_note_from_input(
    input_: InputOutput,
) -> Note:
    llm = LLMExtractNote(config=get_settings().open_ai)
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
                    "Die Kernaussage oder der Titel. Muss den gesamten Sinn erfassen, "
                    "falls kein Body existiert."
                ),
            },
            "content": {
                "type": "string",
                "description": (
                    "Zusätzliche Details oder Kontext. HIER NICHTS SCHREIBEN, wenn der Titel "
                    "bereits die komplette Information enthält (Vermeidung von Redundanz)."
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
        output_type=Note,
    )
    return reply
