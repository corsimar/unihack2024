import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"

def convert_objectid(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def reset_state():
    for key in list(st.session_state.keys()):
        if key != 'role':
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
        st.stop()
    
    if st.session_state.role != allowed_role:
        st.error("You are not authorized to access this page.")
        st.stop()
