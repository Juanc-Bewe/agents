import requests
import streamlit as st
import random
import time
import json
import os

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/interview"

def save_questions_to_file(thread_id, questions):
    # Create a directory for saved questions if it doesn't exist
    os.makedirs('saved_questions', exist_ok=True)
    filename = f'saved_questions/{thread_id}.json'
    with open(filename, 'w') as f:
        json.dump(questions, f)

def load_questions_from_file(thread_id):
    try:
        filename = f'saved_questions/{thread_id}.json'
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def fundamental_agent() -> str:
    print("fundamental_agent executed")
    st.title("🤖 Fundamental Agent")

    # Initialize thread_id in session state if it doesn't exist
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(random.randint(1, 1000000))

    # Load saved questions for this thread when initializing session state
    if "questions_list" not in st.session_state:
        st.session_state.questions_list = load_questions_from_file(st.session_state.thread_id)

    st.sidebar.markdown("## ⚙️ Fundamental Config")
    test_tab = st.sidebar.tabs(["Basic config", "Questions"])

    with test_tab[0]:
        # Get previous thread_id for comparison
        previous_thread_id = st.session_state.thread_id

        # Thread ID input
        thread_id = st.text_input('Thread ID', value=st.session_state.thread_id, 
            help="Save for checkpointer of the conversation")

        # Update thread_id in session state and reload questions if changed
        if thread_id != previous_thread_id:
            st.session_state.thread_id = thread_id
            st.session_state.questions_list = load_questions_from_file(thread_id)
            st.rerun()

        language = st.selectbox(
            'Language',
            ('spanish', 'english', 'portuguese')
        )

    with test_tab[1]:
        questions_tab = st.tabs(["Create", "View"])

        # Create new question section
        with questions_tab[0]:
            with st.expander("Create New Question", expanded=True):
                question = st.text_input("Question", key="new_question")
                criteria = st.text_area("Evaluation Criteria", key="new_criteria", 
                    help="Enter the criteria to evaluate the answer")

                if st.button("Add Question"):
                    if "questions_list" not in st.session_state:
                        st.session_state.questions_list = []

                    if question and criteria:
                        st.session_state.questions_list.append({
                            "question": question,
                            "criteria": criteria
                        })
                        # Clear the inputs by modifying the session state before widget creation
                        st.success("Question added successfully!")
                        time.sleep(1)  # Wait 1 second to show success message
                        st.session_state.pop('new_question', None)
                        st.session_state.pop('new_criteria', None)
                        st.session_state.new_question = ""
                        st.session_state.new_criteria = ""
                        st.rerun()
        # Display questions section
        with questions_tab[1]:
            with st.expander("View Questions List", expanded=True):
                if "questions_list" in st.session_state and st.session_state.questions_list:
                    st.write("Current Questions:")
                    for i, q in enumerate(st.session_state.questions_list):
                        col1, col2 = st.columns([5,1])
                        with col1:
                            st.write(f"{i+1}. Question: {q['question']}")
                            st.write(f"   Criteria: {q['criteria']}")
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
