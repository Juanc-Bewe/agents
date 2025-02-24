import requests
import streamlit as st
import time
import json

URL = "https://backendbeweliteqa.bewe.co/api/v1/ai/onboarding"
URLV2 = "https://backendbeweliteqa.bewe.co/api/v1/ai/onboarding/fundamentals"
URLV2_LOCAL = "http://localhost:9007/api/v1/ai/onboarding/fundamentals"


def load_base_questions():
    with open('questions/base-1.json', 'r') as file:
        return json.load(file)

def fundamental_agent() -> str:
    print("fundamental_agent executed")
    st.title("🤖 Fundamental Agent")

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(int(time.time()))

    st.sidebar.markdown("## ⚙️ Fundamental Config")
    tabs = st.sidebar.tabs(["Basic config", "Questions"])

    with tabs[0]:
        if "config_confirmed" in st.session_state and st.session_state.config_confirmed:
            st.warning("⚠️ Configuration cannot be modified while chat is active. Please refresh the page to start a new session.")
            st.info(f"Thread ID: {st.session_state.thread_id}")
            st.info(f"Language: {st.session_state.language}")
        else:
            # Thread ID input
            st.markdown("#### Load Questions")
            st.markdown("Click to load the default set of questions. ⚠️ Warning: Loading base questions will remove any custom questions you've added. Are you sure?")

            if st.button("Load Base Questions", key="load_questions"):
                st.session_state.questions_list = load_base_questions()
                st.success("Base questions loaded successfully!")
                time.sleep(1)  # Give users time to see the success message
                st.rerun()

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

            main_voice = st.selectbox(
                'Main Voice',
                ('Linda', 'Linda-v2',)
            )

            st.write("")  # Add empty space
            st.write("")  # Add empty space

            # Add confirm button
            if st.button("Start Chat Session"):
                st.session_state.thread_id = thread_id
                st.session_state.language = language
                st.session_state.config_confirmed = True
                st.session_state.questions_list = st.session_state.get("questions_list", [])
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
                    question_id = st.number_input("Question ID", min_value=7, step=1, key="new_question_id", help="Enter a unique ID for the question - this ID must not be used by any other question")
                    question = st.text_input("Question", key="new_question")
                    criteria = st.text_area("Evaluation Criteria", key="new_criteria",
                        help="Enter the criteria to evaluate the answer")
                    example = st.text_area("Example Answer", key="new_example",
                        help="Enter an example of a good answer")

                    if st.button("Add Question"):
                        if "questions_list" not in st.session_state:
                            st.session_state.questions_list = []

                        # Check for duplicate ID
                        existing_ids = [q['id'] for q in st.session_state.questions_list]
                        if question_id in existing_ids:
                            st.error(f"Question ID {question_id} already exists. Please choose a different ID.")
                        elif question and criteria:
                            st.session_state.questions_list.append({
                                "id": question_id,
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

                with st.expander("View Questions List", expanded=True):
                    if "questions_list" in st.session_state and st.session_state.questions_list:
                        st.write("Current Questions:")
                        for i, q in enumerate(st.session_state.questions_list):
                            col1, col2 = st.columns([5,1])
                            with col1:
                                st.write(f"{q['id']}. Question: {q['question']}")
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

    # Accept user input - Add configuration check
    if "config_confirmed" not in st.session_state:
        st.session_state.config_confirmed = False

    if st.session_state.config_confirmed and len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "assistant", "content": "Hola 👋", "audio_file": "./audio/Linda-neutro-v2.mp3"})

    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "audio_file" in message:
                # Autoplay only for the last assistant message
                autoplay = message["role"] == "assistant" and i == ( len(st.session_state.messages) - 1)
                st.audio(message["audio_file"], format='audio/mp3', start_time=0, autoplay=autoplay)

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
                    response = requests.post(URLV2, json={
                        "content": {
                            "type": "text",
                            "content": prompt
                        },
                        "thread_id": st.session_state.thread_id,
                        "account_id": st.session_state.thread_id,
                        "language": st.session_state.language,
                        "base_questions": st.session_state.questions_list,
                    })
                    response_data = response.json()
                    # Get the text from the first content item
                    full_response = response_data['content'][0]['content']
                    print(full_response)
                    message_placeholder.markdown(full_response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response,
                    })


if __name__ == "__main__":
    fundamental_agent()
