import streamlit as st
import os
from search_engine import rrr_snippets, rrr_pages
# App title
st.set_page_config(page_title="🦙💬 LawLinker Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    # if 'REPLICATE_API_TOKEN' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     replicate_api = st.secrets['REPLICATE_API_TOKEN']
    # else:
    #     replicate_api = st.text_input('Enter Replicate API token:', type='password')
    #     if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    #         st.success('Proceed to entering your prompt message!', icon='👉')

    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    st.subheader('Models and parameters')
    
    
    # temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    # top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
    
    # st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')
# os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        full_response = rrr_pages(prompt, n=10)
        st.write(full_response)
        # with st.spinner("Thinking..."):
        #     response = rrr_pages(prompt, n=10)
        #     placeholder = st.empty()
        #     full_response = ''
        #     for item in response:
        #         full_response += item
        #         placeholder.markdown(full_response)
        #     placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)