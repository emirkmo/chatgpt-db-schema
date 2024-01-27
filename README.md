# CHAT GPT Feedback on database table schema 

> [!WARNING]
> This repo was created during the early days of Chat GPT 3.5 hype;
> this is not the way to do things nowadays.

Read json formatted schema for a database table, or a pydantic model that defines the same,
and Ask chatGPT for feedback on the schema including column descriptions. Nice! 

## Code
Tables are implemented using a plugin architecture meaning it is trivial to plugin tables

It uses streamlit & gradio for frontend and has some abstractions
for dealing with the then pretty raw python api wrapper provided by openAI.

Run example dashboard with:

```bash
streamlit run idd_ai/frontend/streamlit.py
```

## Prompt

Very early zero shot prompt. Would be way better using chain of thought here as the task
is easy to split into multiples.

