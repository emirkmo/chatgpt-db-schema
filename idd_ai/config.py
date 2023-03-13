import os


def read_api_key(path: str = "../.env") -> str:
    """Load OpenAI API key from .env file or from environmen variable."""
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    with open(path, "r") as keyfile:
        return keyfile.read().strip("\n").strip().split("=")[1]
