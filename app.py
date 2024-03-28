import os
import openai
import streamlit as st
import time

# Retrieve the API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with the API key
openai.api_key = OPENAI_API_KEY

# Create the Assistant
try:
    assistant = openai.beta.assistants.create(
        name="Test Automation Co-Pilot",
        instructions="You are an AI assistant specialized in software testing. Analyze the provided test scripts/use cases and offer solutions and optimizations based on them.",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo"
    )
except Exception as e:
    st.error(f"An error occurred while creating the Assistant: {e}")
    raise

# Streamlit components
st.title("Test Cases Optimization Assistant")
user_query = st.text_area("Enter your test cases/use cases here to review and hit CTRL+Enter to start processing:", height=150)

if user_query:
    try:
        thread = openai.beta.threads.create()
        message = openai.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_query
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Analyze and suggest optimizations based on the test scripts.",
        )

        with st.spinner("Processing your request..."):
            while True:
                run = openai.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id
                )
                if run.completed_at is not None:
                    break
                time.sleep(7)

            messages = openai.beta.threads.messages.list(thread_id=thread.id)
            st.header("Assistant's Suggestions:")
            for message in messages.data:
                if message.content and message.content[0].text.value.strip() and message.role=="assistant":
                    content = message.content[0].text.value
                else:
                    content = "There is no context for this question."
                st.write(content)
    except Exception as e:
        st.error(f"An error occurred while processing your request: {e}")