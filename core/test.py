import streamlit as st
import os
from search_engine import rrr_snippets, rrr_pages
# App title
st.set_page_config(page_title="💬 LawLinker Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('💬 LawLinker Chatbot')
    "Trợ lý ảo hỗ trợ trả lời các câu hỏi về pháp luật ✅"
    "Core engine sử dụng Gemini Pro của Google"
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Xin chào, tôi có thể giúp gì cho bạn?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Xin chào, tôi có thể giúp gì cho bạn?"}]
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
        with st.spinner("Thinking..."):
            full_response = rrr_pages(prompt, history=st.session_state.messages, n=10)
            st.write(full_response)
        #     response = rrr_pages(prompt, n=10)
        #     placeholder = st.empty()
        #     full_response = ''
        #     for item in response:
        #         full_response += item
        #         placeholder.markdown(full_response)
        #     placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)