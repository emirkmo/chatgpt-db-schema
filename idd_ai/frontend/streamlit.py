import streamlit as st

from idd_ai.chatgpt import get_feedback, load_api_key
from idd_ai.contracts import dynamically_create_pydantic_model, make_contract
from idd_ai.plugins.test_plugin import contract as plugin_contract

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

plugin = st.radio("Select a plugin", options=["Test plugin", "New plugin"])
table_name = ""
table_description = ""

# test_plugin = st.button("Use Test plugin")


def ask_for_columns():
    # Create a text input widget for entering in a column name
    column_name = st.text_input("Enter in a column name", value="")
    # Create a radio button widget for selecting the column type
    column_type = st.radio(
        "Select a column type", options=["integer", "float", "string"]
    )

    # Create a text input widget for entering in a column description
    column_description = st.text_input("Enter in a column description", value="")

    # Create a button to submit the column
    submit_column = st.button("Submit column")

    # If the button is clicked, then return the column name, type, and description
    if submit_column:
        columns.append((column_name, column_type, column_description))


if plugin == "New plugin":
    # Create a text input widget for entering in a table name
    table_name = st.text_input("Enter in a table name", value="")
    # Create a text input widget for entering in a table description
    table_description = st.text_input("Enter in a table description", value="")

    # Create a list to store the columns
    columns = []

    st.write("### Columns")
    st.code(columns)

    # Create a button to add ask for a column
    add_column = st.button("Add column", on_click=ask_for_columns)

    if table_name != "" and table_description != "":
        # Create a button to submit the JSON string
        submit_new_plugin = st.button("Submit table", key="submit_new_plugin")

        # If the button is clicked, then parse the JSON string and print it out
        if submit_new_plugin:
            ModelClass = dynamically_create_pydantic_model(
                table_name=table_name, fields=columns
            )
            contract = make_contract(ModelClass, description=table_description)

            st.write("# Contract")
            st.code(contract, language="json")

            # Wait for chatgpt to be ready with streamlit waiting icon
            st.write("# Waiting for chatgpt to be ready...")
            with st.spinner("Waiting..."):
                # Get feedback from chatgpt
                contract_feedback = get_feedback(contract)

            st.write("# Feedback")
            st.code(contract_feedback, language="json")

            st.code(contract_feedback.choices[0].message.content, language="python")


if plugin == "Test plugin":
    contract = plugin_contract
    st.write("# Test Contract")
    st.code(contract, language="json")

    # Create a button to submit the JSON string
    submit_test_plugin = st.button(
        "Get feedback on test plugin", key="submit_test_plugin"
    )

    # If the button is clicked, then parse the JSON string and print it out
    if submit_test_plugin:

        # Wait for chatgpt to be ready with streamlit waiting icon
        st.write("# Waiting for chatgpt to be ready...")
        with st.spinner("Waiting..."):
            # Get feedback from chatgpt
            contract_feedback = get_feedback(contract)

        st.write("# Feedback")
        st.code(contract_feedback, language="json")

        st.code(contract_feedback.choices[0].message.content, language="python")
