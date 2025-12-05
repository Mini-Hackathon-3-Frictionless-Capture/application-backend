from .repository import GenericLLM


class LLMClassifyAction(GenericLLM):
    template_dir = "classify_action"


class LLMExtractNote(GenericLLM):
    template_dir = "extract_note"


class LLMExtractTask(GenericLLM):
    template_dir = "extract_task"
