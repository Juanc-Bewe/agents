import requests
import streamlit as st
import random

URL = "https://backendbeweliteqa.bewe.co/api/v1/llm/interview"

def interviewer_agent() -> str:
	print("interviewer_agent executed")
	st.title("Helper stream lit")
	st.write("This is a helper streamlit chat command")

	# Initialize thread_id in session state if it doesn't exist
	if "thread_id" not in st.session_state:
		st.session_state.thread_id = str(random.randint(1, 1000000))

	account_id = st.sidebar.text_input('Account ID', value="234234234234")
	thread_id = st.sidebar.text_input('Thread ID', value=st.session_state.thread_id)

	language = st.sidebar.selectbox(

		'Language',
		('spanish', 'english', 'portuguese')
	)
	account_type = st.sidebar.selectbox(
			'Type',
			('barbershops', 'restaurants', 'hotels', 'shopping', 'other')
	)
	if account_type == 'other':
		account_type = st.sidebar.text_input('Other')

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
				response = requests.post(URL, json={
					"answer": prompt,
					"thread_id": thread_id,
					"account_id": account_id,
					"type": account_type,
					"language": language
				})
				full_response = response.json().get("response", "")
				message_placeholder.markdown(full_response)
				st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
	interviewer_agent()
