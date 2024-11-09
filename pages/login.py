import streamlit as st
import utils
if "role" not in st.session_state:
    st.session_state.role = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
# elif st.session_state.role == "professor":
#     utils.login_redirecting("professor")
# elif st.session_state.role == "student":
#     utils.login_redirecting("student")
elif st.session_state.role == "professor" or st.session_state.role == "student":
    utils.login_redirecting()
# Set page title
col1, col2, col3 = st.columns([2,6,2])
# Create login form
with col2:
    st.title("Welcome to RevoLearn!")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

# Handle form submission
if submit_button:
    # if username == "prof@test.com" and password == "password":
    #     st.session_state.role = "professor"
    #     utils.reset_and_navigate("pages/professor_dashboard.py")
    # elif username == "stud@test.com" and password == "password":
    #     st.session_state.role = "student"
    #     utils.reset_and_navigate("pages/student_dashboard.py")    

    # else:
    #     st.error("Invalid username or password")
    if utils.login(username, password) == 1:
        if st.session_state.role == "professor":
            utils.reset_and_navigate("pages/professor_dashboard.py")
        elif st.session_state.role == "student":
            utils.reset_and_navigate("pages/student_dashboard.py")