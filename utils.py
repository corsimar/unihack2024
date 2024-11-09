import streamlit as st
import requests
import hashlib
import time

BACKEND_URL = "http://localhost:5000"

def convert_objectid(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def reset_state():
    for key in list(st.session_state.keys()):
        if key != 'role' and key != 'user_id':
            del st.session_state[key]
    
def reset_and_navigate(page):
    """
    Resets the given state and navigates to the specified page.
    
    Parameters:
    state (dict): The state dictionary to reset.
    page (str): The page to navigate to.
    """
    reset_state()
    st.switch_page(page)

def get_lessons_dashboard():
    response = requests.get(f"{BACKEND_URL}/get-all-lessons")
    if response.status_code == 200:
        lessons = response.json()
    return lessons 

def remove_lesson(lesson_id):
    response = requests.delete(f"{BACKEND_URL}/remove-lesson/{lesson_id}")
    if response.status_code == 200:
        st.success("Lesson removed successfully.")
    else:
        st.error("Failed to remove lesson.")

def restrict_access(allowed_role):
    if 'role' not in st.session_state:
        st.error("You should be logged in to access this page.")
        if st.button("Login"):
            reset_and_navigate("pages/login.py")
        st.stop()
    
    if st.session_state.role != allowed_role:
        st.error("You are not authorized to access this page.")
        st.stop()

def complete_lesson(lesson_id):
    entry = {
        'lesson_id': lesson_id,
        'user_id': st.session_state.user_id
    }
    response = requests.post(f"{BACKEND_URL}/complete-lesson", json=entry)
    if response.status_code == 200:
        st.success("Lesson completed successfully.")
    else:
        st.error("Failed to complete lesson.")
        
def get_completed_lessons():
    user_id = st.session_state.user_id
    response = requests.get(f"{BACKEND_URL}/get-completed-lessons/{user_id}")
    if response.status_code == 200:
        lessons = response.json()
    return lessons

def get_lessons_student():
    user_id = st.session_state.user_id
    response = requests.get(f"{BACKEND_URL}/get-lessons-student/{user_id}")
    if response.status_code == 200:
        lesson_student = response.json()
    return lesson_student

def login(email, password):
    entry = {
        'email': email,
        'password': hash_password(password)
    }
    response = requests.post(f"{BACKEND_URL}/login", json=entry)
    if response.status_code == 200:
        user = response.json()
        st.session_state.user_id = user['_id']
        st.session_state.role = user['role']
        st.success("Login successful.")
        st.write(f"Welcome, {user['name']}!")
        return 1
    elif response.status_code == 404:
        st.error("User not existing.")
        return 0
    elif response.status_code == 401:
        st.error("Incorrect password.")
        return 0
    
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_redirecting():
    if st.session_state.role in ['professor', 'student']:
        st.write("You are already logged in.")
        redirecting = st.empty()
        for i in range(3, 0, -1):
            redirecting.write(f"Redirecting in {i} seconds...")
            time.sleep(1)
        if st.session_state.role == 'professor':
            reset_and_navigate("pages/professor_dashboard.py")
        elif st.session_state.role == 'student':
            reset_and_navigate("pages/student_dashboard.py")
    else:
        st.stop()
        
def logout():
    for key in list(st.session_state.keys()):
            del st.session_state[key]
    st.success("Logout successful.")
    st.write("You have been logged out.")
    reset_and_navigate("pages/login.py")
    
def get_user_xp():
    user_id = st.session_state.user_id
    response = requests.get(f"{BACKEND_URL}/get-user-xp/{user_id}")
    if response.status_code == 200:
        xp = response.json()
    else:
        xp = None
    return xp

def get_locked_lessons():
    user_id = st.session_state.user_id
    response = requests.get(f"{BACKEND_URL}/get-locked-lessons/{user_id}")
    if response.status_code == 200:
        lessons = response.json()
    return lessons

def get_experiment(lesson_id):
    response = requests.get(f"{BACKEND_URL}/get-experiment/{lesson_id}")
    if response.status_code == 200:
        experiment = response.json()
    return experiment