import ollama
import streamlit as st
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
question = st.chat_input("You: ")

# with st.chat_message("User"):
if question:
    st.session_state.messages.append(
        {"role": "user",
         "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        response = ollama.chat(
            model="llama3.2:3b",
            messages=st.session_state.messages)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response["message"]["content"]
    })
    with st.chat_message("assistant"):
        st.write("AI:", response["message"]["content"])

uploaded_file = st.file_uploader("Upload a file...")
if uploaded_file:
    st.write("File uploaded successfully...")
    context = uploaded_file.read().decode("utf-8")
    st.text(context)
