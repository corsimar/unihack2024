import streamlit as st
import utils
import time

if "role" not in st.session_state:
    st.session_state.role = ""
elif st.session_state.role == "professor":
    utils.login_redirecting("professor")
    # utils.reset_and_navigate("pages/professor_dashboard.py")
elif st.session_state.role == "student":
    utils.login_redirecting("student")
    # utils.reset_and_navigate("pages/student_dashboard.py")
# Set page title
st.title("Welcome to RevoLearn!")

# Create login form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Login")

# Handle form submission
if submit_button:
    if username == "prof@test.com" and password == "password":
        st.session_state.role = "professor"
        utils.reset_and_navigate("pages/professor_dashboard.py")
    elif username == "stud@test.com" and password == "password":
        st.session_state.role = "student"
        utils.reset_and_navigate("pages/student_dashboard.py")    

    else:
        st.error("Invalid username or password")