from enum import StrEnum, auto
from typing import TypedDict

from pydantic.dataclasses import dataclass


class ChatRoles(StrEnum):
    """Chat response roles in chat gpt api"""

    system = auto()
    user = auto()
    assistant = auto()


class FormattedChatMessage(TypedDict):
    role: ChatRoles
    content: str


@dataclass
class ChatMessage:
    """Chat message content in chat gpt api"""

    role: ChatRoles = ChatRoles.user
    content: str = ""

    def __post_init__(self):
        if self.content == "":
            raise ValueError("Content should not be empty, else we waste tokens!")

    def _minify_prompt(self) -> str:
        return (
            self.content.replace("  ", "")  # remove visual indent
            .strip()
            .replace("\n", " ")  # remove newlines
            .strip()
            .replace("<br>", "\n")  # add newlines for paragraph breaks only.
        )

    def formatted(self) -> FormattedChatMessage:
        return {"role": self.role, "content": self._minify_prompt()}
