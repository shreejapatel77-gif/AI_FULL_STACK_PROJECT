import streamlit as st
st.title("Welcome to my first app")
st.write("Hello")
name = st.text_input("Enter your name")
if st.button("Submit"):
    st.write("Hello", name)
    chatinput = st.text_input("Enter your email")
