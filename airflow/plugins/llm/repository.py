import json
from enum import Enum
from pathlib import Path
from typing import Any, Literal, TypeVar

from airflow_config import OpenAPIConfig
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from openai.types.chat import ChatCompletionToolUnionParam
from pydantic import BaseModel

T = TypeVar("T")
_T_ACTION_CODE = Literal["identity", "action"]
_T_LANGUAGE_CODE = Literal["en", "de"]


class OpenAIModel(Enum):
    gpt_5_nano = "gpt-5-nano-2025-08-07"
    gpt_5_mini = "gpt-5-mini-2025-08-07"
    gpt_5 = "gpt-5.1-2025-11-13"


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class GenericLLM:
    template_dir: str | None = None

    def __init__(self, config: OpenAPIConfig):
        self.config = config

    def get_client(self):
        return OpenAI(api_key=self.config.secret, project=self.config.project)

    def get_template_dir(
        self,
        language_code: _T_LANGUAGE_CODE,
    ) -> Path:
        if not self.template_dir:
            raise ValueError(f"No template_dir defined for {self.__class__.__name__}")
        repository_dir = Path(__file__).parent / "assets"
        return repository_dir / self.template_dir / language_code

    def get_template_file(
        self,
        language_code: _T_LANGUAGE_CODE,
        template_type: _T_ACTION_CODE,
    ) -> Path:
        template_dir = self.get_template_dir(language_code)
        return template_dir / f"{template_type}.jinja2"

    def get_context(
        self,
        context_input: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if context_input is None:
            context = {}  # type: ignore
            return context
        return context_input

    def get_template(
        self,
        language_code: _T_LANGUAGE_CODE,
        template_type: _T_ACTION_CODE,
        context_input: dict[str, Any] | None = None,
    ) -> str:
        template_dir = self.get_template_dir(language_code)
        template_file_path = self.get_template_file(language_code, template_type)
        if not template_file_path.exists():
            raise FileNotFoundError(f"Template file {template_file_path} not found")

        env = Environment(loader=FileSystemLoader(template_dir))  # nosec B701
        template = env.get_template(template_file_path.name)
        context = self.get_context(context_input)
        return template.render(context)

    def get_identity_prompt(
        self,
        language_code: _T_LANGUAGE_CODE,
        context_input: dict[str, Any] | None = None,
    ):
        return self.get_template(
            language_code=language_code,
            template_type="identity",
            context_input=context_input,
        )

    def get_action_prompt(
        self,
        language_code: _T_LANGUAGE_CODE,
        context_input: dict[str, Any] | None = None,
    ):
        return self.get_template(
            language_code=language_code,
            template_type="action",
            context_input=context_input,
        )

    def perform_prompt(
        self,
        model: OpenAIModel,
        messages: list[Message],
    ):
        pass

    def perform_tool_prompt(
        self,
        model: OpenAIModel,
        messages: list[Message],
        tools: list[ChatCompletionToolUnionParam],
        output_type: type[T],
    ) -> T:
        client = self.get_client()
        messages = [msg.model_dump() for msg in messages]
        completion = client.chat.completions.create(
            model=model.value,
            messages=messages,
            tools=tools,
            tool_choice="required",
        )
        message = completion.choices[0].message

        if not message.tool_calls:
            raise RuntimeError("Tool Calls Expected")
        raw = message.tool_calls[0].function.arguments
        parsed = json.loads(raw)
        return output_type(**parsed)
