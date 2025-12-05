from airflow_config import get_settings
from automation_util.classification.dto import Action
from automation_util.inputs.dto import InputOutput
from llm.llm_templates import LLMClassifyAction
from llm.repository import Message, OpenAIModel
from openai.types.chat import ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition

from airflow.sdk import task


@task
def perform_classification(
    input_: InputOutput,
) -> Action:
    llm = LLMClassifyAction(config=get_settings().open_ai)
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
            "type": {
                "type": "string",
                "enum": ["note", "task"],
                "description": "The type of text input type",
            }
        },
        "required": ["type"],
    }
    tools = ChatCompletionFunctionToolParam(
        type="function",
        function=FunctionDefinition(
            name="perform_input_classification",
            description="Takes a text and responses with a message type",
            parameters=parameters_schema,
        ),
    )
    reply = llm.perform_tool_prompt(
        model=OpenAIModel.gpt_5_mini,
        messages=[identity_message, action_message, user_message],
        tools=[tools],
        output_type=Action,
    )
    return reply
