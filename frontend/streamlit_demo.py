import json
import inspect
from typing import Optional
import logging

import streamlit as st

from idd_ai.chatgpt import get_feedback, load_api_key
from idd_ai.contracts import (
    ensure_valid_contract,
)
from idd_ai.plugins.test_plugin import contract as plugin_contract
from idd_ai.plugins.test_plugin import AddStats

st.title("IDD AI")

# Button to use test plugin contract or enter in a new one
api_key_loaded = False

if not api_key_loaded:
    try:
        load_api_key()
        api_key_loaded = True
    except FileNotFoundError:
        api_key = st.text_input("Enter in your OpenAI API key", value="")
        load_api_key(api_key)
        api_key_loaded = True
    except Exception as e:
        st.write("Error loading API key")
        st.write(e)

valid_contract = False
plugin = st.radio("Select a plugin", options=["New plugin", "Use test plugin"])
# table_name = ""
# table_description = ""

# test_plugin = st.button("Use Test plugin")

st.header(":green[Example contract]")
st.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: x-large;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)
with st.expander("**Source code**", expanded=True):
    st.write("### Test plugin contract source code:")
    st.code(inspect.getsource(AddStats), language="python")

with st.expander("**JSON contract**"):
    st.write("### Test plugin contract JSON:")
    st.code(json.dumps(plugin_contract, indent=4), language="json")


class _Contract_PlaceHolder:
    """Use if rountrip to pydantic model is not needed"""

    def __init__(self, json_contract: str) -> None:
        self.json_contract = json_contract

    def schema(self) -> dict:
        return json.loads(self.json_contract)


contract = plugin_contract
if plugin == "New plugin":

    st.write("## Create new plugin contract from JSON")
    st.write(
        "See example test plugin contract above for reference. JSON should be in the following format:"
    )
    st.write(
        "```json\n{\ntable: ...,\n table_description: ...,\n columns: {\ncolumn_name_1:{\ntype: ...,\n description: ...,}}}```"
    )
    contract_init_value = "{table: ..., table_description: ..., columns: {column_name_1:{type: ..., description: ...,}}}"

    # Create a wide text input widget for entering in json contract

    with st.expander("**Enter New JSON contract**"):

        # use_test_contract = st.button("Use test contract")
        # if use_test_contract:
        #     contract_init_value = json.dumps(plugin_contract, indent=4).replace(
        #         "'", "`"
        #     )
        if not valid_contract:
            typed_contract = st.text_area(
                label="Edit JSON below. If using test contract, make sure to type some text to trigger the input form.",
                value=contract_init_value,
                height=500,
            )
            # Create a button to submit the JSON string
            validate_json = st.button("Validate json", key="submit_new_plugin")

    # If the button is clicked, then parse the JSON string and print it out
    if validate_json and not valid_contract:
        contract_json = json.loads(typed_contract)

        # logging.debug(contract_json)
        # logging.debug(typed_contract)

        if ensure_valid_contract(contract_json):
            logging.debug("Valid contract!")
            st.write("Valid contract!")
            # @TODO: This is roundtrip to pydantic model is probably not needed.
            # Create a pydantic model from contract (indirectly validates, I think)
            # contract_model = pydantic_model_from_contract(contract_json)

            # Parse the JSON string
            #  contract = make_contract(contract_model)
            contract = contract_json
            valid_contract = True

if plugin == "Use test plugin":
    contract = plugin_contract
    valid_contract = True

feedback: Optional[str] = None
if valid_contract:
    st.write("# Proposed Contract:")
    st.code(json.dumps(contract, indent=4), language="json")

    # Create a button to submit the JSON string
    submit_test_plugin = st.button(
        "Get feedback on proposed plugin contract", key="submit_test_plugin"
    )

    # If the button is clicked, then parse the JSON string and print it out
    got_feedback = False
    if submit_test_plugin:

        # Wait for chatgpt to be ready with streamlit waiting icon
        st.write("### Waiting for ChatGPT's valuable insight...")
        with st.spinner("Waiting..."):
            # Get feedback from chatgpt
            contract_feedback = get_feedback(contract)
            got_feedback = True

        with st.expander("ChatGPT raw response"):
            st.code(contract_feedback, language="json")

        if got_feedback:
            feedback = contract_feedback.choices[0].message.content

    if got_feedback and feedback:
        st.header("Feedback")
        st.code(feedback, language="python")
        st.markdown(feedback)
