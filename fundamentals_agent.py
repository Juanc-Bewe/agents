import requests
import streamlit as st
import random
import time
import json
import os

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/onboarding"

def load_base_questions():
    with open('questions/base-1.json', 'r') as file:
        return json.load(file)

def fundamental_agent() -> str:
    print("fundamental_agent executed")
    st.title("🤖 Fundamental Agent")

    # Initialize thread_id in session state if it doesn't exist
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(int(time.time()))

    # Load saved questions for this thread when initializing session state

    st.sidebar.markdown("## ⚙️ Fundamental Config")
    tabs = st.sidebar.tabs(["Basic config", "Questions"])

    with tabs[0]:
        if "config_confirmed" in st.session_state and st.session_state.config_confirmed:
            st.warning("⚠️ Configuration cannot be modified while chat is active. Please refresh the page to start a new session.")
            st.info(f"Thread ID: {st.session_state.thread_id}")
            st.info(f"Language: {st.session_state.language}")
        else:
            # Thread ID input
            thread_id = st.text_input('Thread ID', value=st.session_state.thread_id,
                help="Save for checkpointer of the conversation")

            language = st.selectbox(
                'Language',
                ('spanish', 'english', 'portuguese')
            )

            # Add confirm button
            if st.button("Confirm Configuration"):
                st.session_state.thread_id = thread_id
                st.session_state.language = language
                st.session_state.config_confirmed = True
                st.success("Configuration confirmed!")
                st.rerun()

    with tabs[1]:
        if "config_confirmed" in st.session_state and st.session_state.config_confirmed:
            st.warning("⚠️ Configuration cannot be modified while chat is active. Please refresh the page to start a new session.")
            questions_tab = st.tabs(["Questions", "Add"])

            # Display questions section
            with questions_tab[0]:
                with st.expander("View Questions List", expanded=True):
                    if "questions_list" in st.session_state and st.session_state.questions_list:
                        st.write("Current Questions:")
                        for i, q in enumerate(st.session_state.questions_list):
                            col1, col2 = st.columns([5,1])
                            with col1:
                                st.write(f"{i+1}. Question: {q['question']}")
                                st.write(f"   Criteria: {q['criteria']}")
                                st.write(f"   Example: {q.get('example', 'No example provided')}")
                    else:
                        st.info("No questions added yet.")
        else:
            questions_tab = st.tabs(["Questions", "Add"])

            # Create new question section
            with questions_tab[1]:
                with st.expander("Create New Question", expanded=True):
                    question = st.text_input("Question", key="new_question")
                    criteria = st.text_area("Evaluation Criteria", key="new_criteria",
                        help="Enter the criteria to evaluate the answer")
                    example = st.text_area("Example Answer", key="new_example",
                        help="Enter an example of a good answer")

                    if st.button("Add Question"):
                        if "questions_list" not in st.session_state:
                            st.session_state.questions_list = []

                        if question and criteria:
                            st.session_state.questions_list.append({
                                "question": question,
                                "criteria": criteria,
                                "example": example
                            })
                            st.success("Question added successfully!")
                            time.sleep(1)
                            st.session_state.pop('new_question', None)
                            st.session_state.pop('new_criteria', None)
                            st.session_state.pop('new_example', None)
                            st.session_state.new_question = ""
                            st.session_state.new_criteria = ""
                            st.session_state.new_example = ""
                            st.rerun()

            # Display questions section with delete buttons
            with questions_tab[0]:
                if st.button("Load Base questions", key="load_questions"):
                    st.session_state.questions_list = load_base_questions()
                    st.rerun()

                with st.expander("View Questions List", expanded=True):
                    if "questions_list" in st.session_state and st.session_state.questions_list:
                        st.write("Current Questions:")
                        for i, q in enumerate(st.session_state.questions_list):
                            col1, col2 = st.columns([5,1])
                            with col1:
                                st.write(f"{i+1}. Question: {q['question']}")
                                st.write(f"   Criteria: {q['criteria']}")
                                st.write(f"   Example: {q.get('example', 'No example provided')}")
                            with col2:
                                if st.button("🗑️", key=f"delete_{i}"):
                                    st.session_state.questions_list.pop(i)
                                    st.rerun()
                    else:
                        st.info("No questions added yet.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input - Add configuration check
    if "config_confirmed" not in st.session_state:
        st.session_state.config_confirmed = False

    if not st.session_state.config_confirmed:
        st.warning("Please confirm the configuration in the sidebar before starting the chat.")
    elif prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        print(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                # full_response = "Lo sentimos, esta funcionalidad se encuentra actualmente en desarrollo. Nuestro equipo está trabajando diligentemente para implementar esta característica. Por favor, vuelva a intentarlo más tarde."
                response = requests.post(URL, json={
                    "message": prompt,
                    "thread_id": st.session_state.thread_id,
                    "language": st.session_state.language,
                    "base_questions": st.session_state.questions_list
				})
                print(response.json())
                full_response = response.json().get("message", "")
                message_placeholder.markdown(full_response)
                # //google how to append a list of messages
                st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    fundamental_agent()
