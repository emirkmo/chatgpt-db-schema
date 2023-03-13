from idd_ai.chatgpt import get_plugin_feedback, load_api_key
from idd_ai.plugins import plugins
from idd_ai.usage import print_useage_cost


def main() -> None:
    load_api_key()
    for plugin in plugins:
        feedbacks = get_plugin_feedback(plugin)
        for feedback in feedbacks:
            print_useage_cost(feedback)


# if __name__ == "__main__":
#     main()
