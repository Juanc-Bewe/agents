import os
import requests
import streamlit as st
import time

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/chat/client"
# URL = "http://localhost:9007/api/v1/llm/chat/client"


def clients_chat() -> str:
    print("clients_chat executed")
    st.title("🤖 Clients Chat")

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(int(time.time()))

    st.sidebar.markdown("## ⚙️ Clients Chat Config")
    tabs = st.sidebar.tabs(["Basic config"])

    with tabs[0]:
        if "config_confirmed" in st.session_state and st.session_state.config_confirmed:
            st.warning("⚠️ Configuration cannot be modified while chat is active. Please refresh the page to start a new session.")
            st.info(f"Thread ID: {st.session_state.thread_id}")
            st.info(f"Account ID: {st.session_state.account_id}")
            st.info(f"Language: {st.session_state.language}")
            st.info(f"Enterprise ID: {st.session_state.enterprise_id}")
            st.info(f"Enterprise Name: {st.session_state.enterprise_name}")
            st.info(f"Name Assistant: {st.session_state.name_assistant}")
        else:
            # Thread ID input
            thread_id = st.text_input('Thread ID', value=st.session_state.thread_id,
                help="Save for checkpointer of the conversation")

            # Account ID input
            account_id = st.text_input('Account ID', value=st.session_state.get('account_id', ''),
                help="Enter the account identifier (required)")

            # Or Option 2: Using a dictionary
            language_options = {
                'Spanish': 'es',
                'English': 'en',
                'Portuguese': 'pt'
            }
            language = st.selectbox(
                'Language',
                options=list(language_options.keys())
            )
            language = language_options[language]

            # Enterprise ID input
            enterprise_id = st.text_input('Enterprise ID', value=st.session_state.get('enterprise_id', ''),
                help="Enter the enterprise identifier (required)")

            # Enterprise Name input
            enterprise_name = st.text_input('Enterprise Name', value=st.session_state.get('enterprise_name', ''),
                help="Enter the enterprise name (required)")

            # Name Assistant input
            name_assistant = st.text_input('Name Assistant', value=st.session_state.get('name_assistant', ''),
                help="Enter the name of the assistant (required)")

            st.write("")  # Add empty space
            st.write("")  # Add empty space

            # Add confirm button with account_id validation
            if st.button("Start Chat Session"):
                if not account_id:
                    st.error("Account ID is required to start the chat session.")
                else:
                    st.session_state.thread_id = thread_id
                    st.session_state.account_id = account_id
                    st.session_state.language = language
                    st.session_state.config_confirmed = True
                    st.session_state.enterprise_id = enterprise_id
                    st.session_state.enterprise_name = enterprise_name
                    st.session_state.name_assistant = name_assistant
                    st.success("Configuration confirmed!")
                    st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Accept user input - Add configuration check
    if "config_confirmed" not in st.session_state:
        st.session_state.config_confirmed = False

    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.config_confirmed:
        st.warning("Please confirm the configuration in the sidebar before starting the chat.")
    else:
        if prompt := st.chat_input("What is up?"):
            # Add user message to chat history
            # if "messages" not in st.session_state:
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
                print(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = requests.post(URL, json={
                        "content": {
                            "type": "text",
                            "content": prompt
                        },
                        "account_id": st.session_state.account_id,
                        "thread_id": st.session_state.thread_id,
                        "language": st.session_state.language,
                        "enterprise_id": st.session_state.enterprise_id,
                        "enterprise_name": st.session_state.enterprise_name,
                        "name_assistant": st.session_state.name_assistant,
                    })
                    response_data = response.json()
                    # Get the text from the first content item
                    full_response = response_data["content"][0]["content"]
                    print(full_response)
                    message_placeholder.markdown(full_response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response,
                    })


if __name__ == "__main__":
    clients_chat()
