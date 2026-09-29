import ollama
import streamlit as st
st.title(":rainbow[*My Chatbot!!!😍*]")
with st.sidebar:
    personalities = {
        "Kid😎": "Give the answers like you are explaining to a 5 year old kid.Give the answer in 2 lines only",
        "Professor👨‍🏫": "You are an IIT professor.Explain the topics using correct terminology.Give the answer in 2-3 lines only",
        "Friendly👥": "You are a friend.Explain about friendship.Give the answer in 2-3 lines only"
    }
    personality = st.selectbox("Select a personality", personalities.keys())
    if st.button("clear chat"):
        st.session_state.messages = []
        st.success("chat cleared successfully")
    st.header("*CHAT SETTINGS*")
    uploaded_file = st.file_uploader("Upload a file...")
    if uploaded_file:
        st.success("File uploaded successfully...")
        with st.expander("Preview"):
            # if st.button("Display"):
            context = uploaded_file.read().decode("utf-8")
            st.text(context)
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
            messages=[{
                "role": "system", "content": personalities[personality]
            }] + st.session_state.messages)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["message"]["content"]
    })
    with st.chat_message("assistant"):
        st.write("AI:", response["message"]["content"])
        st.snow()
