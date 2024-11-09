import streamlit as st
st.title("Welcome to RevoLearn!")

st.write(st.session_state.lesson_name)
st.write(st.session_state.lesson_content)