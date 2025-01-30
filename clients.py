import requests
import streamlit as st
import time
import json

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/chat/client"
URL_DEV = "http://localhost:9007/api/v1/llm/chat/client"

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
            st.info(f"Language: {st.session_state.language}")
        else:
            # Thread ID input
            thread_id = st.text_input('Thread ID', value=st.session_state.thread_id,
                help="Save for checkpointer of the conversation")

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

            st.write("")  # Add empty space
            st.write("")  # Add empty space

            # Add confirm button
            if st.button("Start Chat Session"):
                st.session_state.thread_id = thread_id
                st.session_state.language = language
                st.session_state.config_confirmed = True
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
                        "message": prompt,
                        "account_id": st.session_state.thread_id,
                        "thread_id": st.session_state.thread_id,
                        "language": st.session_state.language,
                    })
                    response_data = response.json()
                    # Get the text from the first content item
                    full_response = response_data["message"]
                    print(full_response)
                    message_placeholder.markdown(full_response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response,
                    })


if __name__ == "__main__":
    clients_chat()
