import streamlit as st
from streamlit_quill import st_quill
import requests
import utils
import time

utils.restrict_access('professor')


st.set_page_config(page_title="Lesson Editor", page_icon="📄", initial_sidebar_state="collapsed", layout='wide')
st.markdown(
    """
<style>
    [data-testid="stBaseButton-headerNoPadding"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
hide_streamlit_style = """
<style>
.stAppHeader {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

BACKEND_URL = "http://localhost:5000"


# Custom CSS to make the button the same height as the text input
st.markdown("""
    <style>
    .submit-button {
        height: 68px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'show_prompt' not in st.session_state:
    st.session_state.show_prompt = False
if 'lesson_xp' not in st.session_state:
    st.session_state.lesson_xp = 0
if 'title' not in st.session_state:
    st.session_state.title = ""
if 'previous_lesson_id' not in st.session_state:
    st.session_state.previous_lesson_id = ""
if 'experiment_id' not in st.session_state:
    st.session_state.experiment_id = ""
if 'show_editor' not in st.session_state:
    st.session_state.show_editor = False
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""
if 'content' not in st.session_state:
    st.session_state.content = ""
if 'show_preview' not in st.session_state:
    st.session_state.show_preview = False

progress = st.progress(1)
steps = 5  # Number of steps in the wizard
progress.progress(st.session_state.current_step / steps)
@st.dialog("Preview Content")
def preview_dialog(content):
    st.header(st.session_state.title)
    st.write(content)
    
if st.session_state.current_step == 1:
    headcol1, headcol2 = st.columns(2)
    with headcol1:
        st.header("Lesson title")
        title = st.text_input("", value=st.session_state.title)
    with headcol2:
        st.header("Lesson xp")
        xp = st.number_input("", value=st.session_state.lesson_xp)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", key="cancel", help="Cancel editing", use_container_width=True):
            utils.reset_and_navigate("pages/professor_dashboard.py")
    with col2:
        if st.button("Next", key="goTo2", help="Proceed to the next step", use_container_width=True):
            if title.strip() == "":
                st.warning("Title cannot be empty.")
            elif xp <= 0:
                st.warning("XP should be a number greater than 0.")
            else:
                st.session_state.title = title
                st.session_state.lesson_xp = int(xp)
                st.session_state.current_step = 2
                progress.progress(st.session_state.current_step / steps)
                st.rerun()
            
if st.session_state.current_step == 2:
    st.header("Should this lesson succeed another lesson?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="goBackTo1", help="Go to previous step", use_container_width=True):
            st.session_state.current_step = 1
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
        
    with col2:
        if st.button("No, this lesson is standalone", key="no", use_container_width=True):
            st.session_state.show_prompt = True
            st.session_state.show_editor = False
            st.session_state.prompt = ""
            st.session_state.content = ""
            st.session_state.show_preview = False
            st.session_state.current_step = 3
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
    
    #add spinner
    with st.spinner('Loading previous lessons...'):
        response = requests.get(f"{BACKEND_URL}/get-previous-lessons")
        if response.status_code == 200:
            lessons = response.json()
            for lesson in lessons:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    pass
                with col2:
                    st.write(lesson['title'])
                    if st.button(f"Select", key=f"select_{lesson['_id']}", use_container_width=True):
                        st.session_state.previous_lesson_id = lesson['_id']
                        st.session_state.show_prompt = True
                        st.session_state.show_editor = False
                        st.session_state.prompt = ""
                        st.session_state.content = ""
                        st.session_state.show_preview = False
                        st.session_state.current_step = 3
                        progress.progress(st.session_state.current_step / steps)
                        st.rerun()
                with col3:
                    pass
        else:
            st.error("Error: Could not fetch previous lessons.")
            
if st.session_state.current_step == 3:
    st.header("Should this lesson include an experiment?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="goBackTo2", help="Go to previous step", use_container_width=True):
            st.session_state.current_step = 2
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
        
    with col2:
        if st.button("No, this lesson doesn't include an experiment", key="no", use_container_width=True):
            st.session_state.show_prompt = True
            st.session_state.show_editor = False
            st.session_state.prompt = ""
            st.session_state.content = ""
            st.session_state.show_preview = False
            st.session_state.current_step = 4
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
    
    
    # Show the experiments with select option
    with st.spinner('Loading experiments...'):
        response = requests.get(f"{BACKEND_URL}/get-experiments")
        if response.status_code == 200:
            experiments = response.json()
            st.header("Select an experiment to include in the lesson")
            # Show each experiment title, description and xp gained and a select button that leads to the next step and adds the experiment in the session_state.experiment
            for experiment in experiments:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    pass
                with col2:
                    st.write(f"{experiment['title']} - {experiment['xp']} XP")
                    st.write(experiment['description'])
                    if st.button(f"Select", key=f"select_{experiment['_id']}", use_container_width=True):
                        st.session_state.current_step = 4
                        st.session_state.experiment_id = experiment['_id']
                        progress.progress(st.session_state.current_step / steps)
                        st.rerun()
                with col3:
                    pass
        else:
            st.error("Error: Could not fetch experiments.")
            
if st.session_state.current_step == 4:
    st.header("What should be the content of this lesson?")
    prompt = st.text_input("", placeholder="Enter the topic for your lesson")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back", key="goBackTo2", help="Cancel editing", use_container_width=True):
            st.session_state.current_step = 3
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
    with col2:
        if st.button("Start from scratch", key="startFromScratch", help="Start from scratch", use_container_width=True):
            st.session_state.content = ""
            st.session_state.current_step = 5
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
    with col3:
        if st.button("Submit", key="submit", help="Submit your prompt", use_container_width=True):
            if prompt:
                st.session_state.prompt = prompt
                with st.spinner('Generating lesson...'):
                    # Make a request to the backend to generate the lesson
                    response = requests.get(f"{BACKEND_URL}/generate-lesson", params={"topic": prompt})
                    
                    if response.status_code == 200:
                        st.session_state.content = response.json()
                        st.session_state.current_step = 5
                        progress.progress(st.session_state.current_step / steps)
                        st.rerun()
                    else:
                        st.session_state.content = "Error: Could not generate lesson."
                        st.session_state.show_editor = False
            else:
                st.warning("Please enter a prompt.")

if st.session_state.current_step == 5:
    
    st.header("Edit your lesson")
    content = st_quill(value=st.session_state.content)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back", key="goBackTo4", help="Cancel editing", use_container_width=True):
            st.session_state.current_step = 4
            progress.progress(st.session_state.current_step / steps)
            st.rerun()
    with col2:
        if st.button("Preview", key="preview", help="Preview your content", use_container_width=True):
            if content:
                preview_dialog(st.session_state.content)
            else:
                st.session_state.show_preview = False
    with col3:
        if st.button("Save", key="save", help="Save your content", use_container_width=True):
            if content.strip() == "":
                st.error("Error: Content cannot be empty.")
            elif st.session_state.prompt.strip() == "":
                st.error("Error: Topic cannot be empty.")
            else:
                lesson_data = {
                    "title": st.session_state.title,
                    "xp": st.session_state.lesson_xp,
                    "content": content,
                    "previous_lesson_id": st.session_state.previous_lesson_id,
                    "experiments": st.session_state.experiment_id,
                }
                response = requests.post(f"{BACKEND_URL}/add-lesson", json=lesson_data)
                if response.status_code == 200:
                    st.success("Lesson added successfully!")
                    time.sleep(2)
                    utils.reset_and_navigate("pages/professor_dashboard.py")
                else:
                    st.error("Error: Could not save lesson.")
