import gradio as gr
from loguru import logger

from idd_ai.chatgpt import load_api_key, ask_chatgpt
from idd_ai.chat import ChatRoles, ChatMessage
from idd_ai.prompts import compose_prompt

# Button to use test plugin contract or enter in a new one
api_key_loaded = False


if not api_key_loaded:
    load_api_key()
    api_key_loaded = True
    # except FileNotFoundError:
    #     # demo = gr.Interface(fn=load_api_key, inputs="API-Key", outputs="text")
    #     api_key_loaded = True


def get_init_message() -> list[ChatMessage]:
    return [
        ChatMessage(
            role=ChatRoles.system,
            content=(
                "You are a helpful and knowledgeable"
                "database expert called IDD AI Assistant, but you have a love"
                "of Swedish Fika buns and desserts and constantly ask to be fed more"
                "of them to answer any more questions."
            ),
        ),
        ChatMessage(
            role=ChatRoles.assistant,
            content=(
                "Hi, I'm the IDD Assistant."
                "I'm here to help you with your database questions."
                "What is your database related question? Please also"
                "prepare your Swedish Fika buns and dessert offerings."
            ),
        ),
    ]


def get_contents(history: list[ChatMessage]) -> list[tuple[str, str]]:
    return [
        (history[i].content, history[i + 1].content)
        for i in range(0, len(history) - 1, 2)
    ]


def submit_init_message(message: str, history):
    history = get_init_message()
    return get_contents(history), history


def talk_to_chatgpt(message: str, history):
    # global message_history
    if len(history) == 0:
        history = get_init_message()

    history.append(ChatMessage(role=ChatRoles.user, content=message))
    prompt = compose_prompt(history)

    response = ask_chatgpt(prompt)
    response_message: str = response["choices"][0]["message"]["content"]

    history.append(ChatMessage(role=ChatRoles.assistant, content=response_message))

    # cost_text = get_query_cost(response)

    return get_contents(history), history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    message_history = get_init_message()
    state = gr.State([])  # type: ignore

    with gr.Row():
        init_text = gr.Textbox(
            show_label=False,
            placeholder="Initialized Message Will appear here, ignore",
            disabled=True,
        ).style(container=False)

    with gr.Row():
        input_text = gr.Textbox(
            show_label=False, placeholder="Type to IDD AI Assistant"
        ).style(container=False)
        logger.info(str(state))
        logger.info(input_text)

    init_text.submit(submit_init_message, [init_text, state], [chatbot, state])
    init_text.submit(lambda: " ", None, init_text)  # clear input text

    input_text.submit(talk_to_chatgpt, [input_text, state], [chatbot, state])
    input_text.submit(lambda: " ", None, input_text)  # clear input text
    logger.info(str(state))
logger.info(str(state))
demo.launch()
