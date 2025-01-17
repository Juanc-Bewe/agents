import requests
import streamlit as st
import random
import time
import json
import os

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/interview"

def load_base_questions():
    with open('questions/base-1.json', 'r') as file:
        return json.load(file)

def fundamental_agent() -> str:
    print("fundamental_agent executed")
    st.title("🤖 Fundamental Agent")

    # Initialize thread_id in session state if it doesn't exist
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(random.randint(1, 1000000))

    # Load saved questions for this thread when initializing session state

    st.sidebar.markdown("## ⚙️ Fundamental Config")
    tabs = st.sidebar.tabs(["Basic config", "Questions"])

    with tabs[0]:

        # Thread ID input
        thread_id = st.text_input('Thread ID', value=st.session_state.thread_id,
            help="Save for checkpointer of the conversation")

        language = st.selectbox(
            'Language',
            ('spanish', 'english', 'portuguese')
        )

    with tabs[1]:
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

        # Display questions section
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

    # Accept user input
    if prompt := st.chat_input("What is up?"):
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
                # response = requests.post(URL, json={
                # 	"answer": prompt,
                # 	"thread_id": thread_id,
                # 	"account_id": account_id,
                # 	"type": account_type,
                # 	"language": language,
                # 	"question_quantity": "question_quantity"
                # })
                # full_response = response.json().get("response", "Esto por ahora es siempre lo mismo")
                full_response = "Esto por ahora es siempre lo mismo"
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    fundamental_agent()
