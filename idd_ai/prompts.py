import itertools
import json
from idd_ai.chat import ChatMessage, FormattedChatMessage, ChatRoles
from idd_ai.contracts import Contract

USER_DEFAULT_PROMPT = """
    You are going to give detailed helpful suggestions to improve the cohesion, readability,
    and ease of use of a proposed SQL database table schema. I will provide a JSON formatted prompt
    starting with a table name, a one-sentence description of the contents of the table
    and what the expected usecase for the data that will be uploaded to this table.
    The usecases are usually analytics or diagnostics for data uploaded by a set of devices sold by a business.
    The prompt will continue with a list of proposed column names, data type of the column,
    and description of the content. <br>

    Using your expertise in database management, data analysis,
    and speaking as someone who must ensure that the names of data fields are consistent,
    descriptive and easy to understand, you will propose helpful changes to the JSON formatted
    table schema, while concisely explaining your reasoning behind your proposed changes. You
    must answer in a concise and space efficient way, providing deeper reasoning if later asked. <br>

    When proposing changes, you will ensure that the column names use a uniform pythonic
    format with underscores "_" to connect words and mention the units of the measurement
    if relevant. For example, columns counting something should end with "_counts", a time measurement
    should include "_seconds" or "_ms" depending on the data measurement unit. <br>

    You will spend the most effort making absolutely sure that the column names are descriptive
    and specific, the column names are easy to read and understand by users who may
    not be familiar with the underlying device or data, in general are easy to read and understand at a glance,
    and that they are uniform in style, formatting, structure, and follow a uniform naming convention.
    This means that the column names and descriptions are not overly generic, unclear, or unspecific.
    They do not use different words to refer to the same things.
    You will also check the spelling and grammar of the descriptions of the columns. <br>

    If you find that you need to propose a large amount of changes, you will limit yourself to only
    proposing what to change, without explaining the reasoning behind it. If you find that the prompt with
    the table columns and descriptions is already very good with a uniform style and clear naming conventions,
    you can explain more of your reasoning since you will only propose minimal changes.
"""

ASSISTANT_DEFAULT_RESPONSE = """Sure, I can help with improving the SQL schema.
    Please provide me with the table name, description, and column names with data type and description,
    in JSON format, so I can propose useful suggestions for improving the SQL schema."""

FOLLOWUP_PROMPT = """I fixed the SQL Schema according to your suggestions.
    Do you see any other mistakes with the JSON formatted SQL Schema?
    Please also check spelling and grammar."""


def compose_prompt(*messages: list[ChatMessage]) -> list[FormattedChatMessage]:
    _messages = itertools.chain.from_iterable(messages)
    return [message.formatted() for message in _messages]


def get_init_prompt() -> list[ChatMessage]:
    system = ChatMessage(
        role=ChatRoles.system,
        content="You are a helpful assistant. Answer as concisely as possible.",
    )

    user = ChatMessage(role=ChatRoles.user, content=USER_DEFAULT_PROMPT)

    assistant = ChatMessage(
        role=ChatRoles.assistant, content=ASSISTANT_DEFAULT_RESPONSE
    )

    return [system, user, assistant]


def make_final_prompt(
    contract: Contract, *additional_prompts: ChatMessage
) -> list[FormattedChatMessage]:
    table_schema_prompt = ChatMessage(content=json.dumps(contract))
    final_prompt = compose_prompt(
        get_init_prompt(), [table_schema_prompt], [*additional_prompts]
    )
    return final_prompt


def make_followup_prompt(
    initial_contract: Contract, initial_feedback: str, fixed_contract: Contract
) -> list[FormattedChatMessage]:


    additional_messages = [
        ChatMessage(
            role=ChatRoles.assistant,
            content=initial_feedback.replace("\n", "<br>"),
        ),
        ChatMessage(
            content=f"{FOLLOWUP_PROMPT} \n\n {json.dumps(fixed_contract)}"
        ),
    ]
    return make_final_prompt(initial_contract, *additional_messages)