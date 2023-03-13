from enum import StrEnum
from typing import Optional, cast

import openai
from openai.openai_object import OpenAIObject

from idd_ai.chat import FormattedChatMessage
from idd_ai.config import read_api_key
from idd_ai.contracts import Contract
from idd_ai.plugins import FixedPlugin, Plugin, has_fixed_contract
from idd_ai.prompts import make_final_prompt, make_followup_prompt


def load_api_key(
    env_name: str = "OPENAI_API_KEY", path: str = ".env", key: Optional[str] = None
) -> None:
    """Load OpenAI API key from .env file or from environment variable
    or via argument."""
    if key is None:
        key = read_api_key(path)
    openai.api_key = key


class ChatModels(StrEnum):
    gpt_turbo = "gpt-3.5-turbo"
    davinci_02 = "text-davinci-002"
    code_davinci = "code-davinci-002"  # 8000 tokens!


def ask_chatgpt(
    prompt: list[FormattedChatMessage], model: ChatModels = ChatModels.gpt_turbo
) -> OpenAIObject:
    completion = openai.ChatCompletion.create(model=model, messages=prompt)
    return cast(OpenAIObject, completion)


def get_feedback(
    contract: Contract, model: ChatModels = ChatModels.gpt_turbo
) -> OpenAIObject:
    final_prompt = make_final_prompt(contract)
    return ask_chatgpt(final_prompt)


def pretty_print_response(feedback: OpenAIObject):
    print(feedback.choices[0].message.content)
    return feedback.choices[0]


def get_follow_up_feedback(
    initial_contract: Contract, initial_feedback: OpenAIObject, fixed_contract: Contract
):

    prompt = make_followup_prompt(
        initial_contract, initial_feedback.choices[0].message.content, fixed_contract
    )
    return ask_chatgpt(prompt)


def print_contract_feedback(contract: Contract) -> OpenAIObject:
    print(contract)
    contract_feedback = get_feedback(contract)
    pretty_print_response(contract_feedback)
    return contract_feedback


def get_plugin_feedback(plugin: Plugin | FixedPlugin) -> tuple[OpenAIObject, ...]:
    """Prints the contract and feedback for a plugin. If the plugin has a fixed
    contract, it will also print the fixed contract and feedback."""
    contract_feedback = print_contract_feedback(plugin.contract)
    if not has_fixed_contract(plugin):
        return (contract_feedback,)

    fixed_contract_feedback = print_contract_feedback(plugin.fixed_contract)
    return (contract_feedback, fixed_contract_feedback)
