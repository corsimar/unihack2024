import streamlit as st
import streamlit.components.v1 as components
import utils
from streamlit_extras.stylable_container import stylable_container 

#utils.restrict_access("student")

# Sample data
roadmap = ["Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4"]
completed_lessons = 2
total_lessons = len(roadmap)
xp = 150

# Initialize session state variables
if 'lesson_name' not in st.session_state:
    st.session_state.lesson_name = ""
if 'lesson_content' not in st.session_state:
    st.session_state.lesson_content = ""

def get_lesson_icon(index):
    if index < completed_lessons:
        return "https://img.icons8.com/ios-filled/50/4CAF50/checkmark.png"
    elif index == completed_lessons:
        return ""
    else:
        return "https://img.icons8.com/ios-filled/50/808080/lock.png"
# Display the roadmap with borders, icons, and progress

st.markdown("""
    <style>
    html, body {
        background: linear-gradient(to bottom, #f0f0f0, #ffffff);
    }
    .lesson {
        font-size: 18px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #333;
    border: 2px solid transparent;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
    transition: all 0.3s;
    border-color: white;
    }
    .lesson:hover {
    border: 4px solid white;
    box-shadow: 0px 0px 10px rgba(76, 175, 80, 0.5);
    }
    .lesson.completed {
        color: #4CAF50;
        border-color: #4CAF50;
    }
    .lesson.locked {
        color: #808080;
        border-color: #808080;
        opacity: 0.5;
        filter: grayscale(100%);
    }
    .lesson span {
        font-size: 18px;
    }
    .lesson img {
        width: 20px;
        height: 20px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .header-text {
        font-size: 2em;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
col1, col2 = st.columns([8.7, 1.3])
with col1:
    st.markdown('<h2 class="header-text">Hello, student!</h2>', unsafe_allow_html=True)
with col2:
    with stylable_container( key="logout",
            css_styles=""" 
            button {
                margin-top: 20px;
                color: white;
                background-color: red;
            }
            button:hover {
                border: 1px transparent black;
            }
                """,):
        if st.button("Logout"):
            utils.logout()


# Display progress bar
with st.spinner("Loading..."):
    lessons = utils.get_lessons_dashboard()
    if len(lessons) == 0:
         with stylable_container(
            css_styles="""
            img {
                 display: block;
  margin-right: auto;
    margin-left: 80%;
    margin-top: 10%;
            filter: brightness(0) invert(0.6);}
            .noLessons {
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: gray;
            }
            """,
            key="no_lessons"
        ):
            st.image("https://cdn-icons-png.freepik.com/256/1466/1466623.png?semt=ais_hybrid")
            st.write('<div class="noLessons">There are no lessons yet. Once your professor starts adding them, they will be visible here.</div>', unsafe_allow_html=True)
    else:    
        progress_percentage = (completed_lessons / total_lessons)
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
            <div style="margin-left: 20px;">
                <h3 style="margin: 0; font-size: 24px; color: #4CAF50;">XP: {xp}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_percentage)
                # Display XP
        
        with stylable_container(
            key="green_button",
            css_styles="""
                button {
                    color: white;
                    border-radius: 6px;
                    line-height: 25px;
                    display: flex;
                    justify-content: flex-start;
                    padding-left: 10px; /* Optional: Adds padding on the left side */
                }
                .st-emotion-cache-3lmqu2 e1nzilvr5 {
                    background-color: #4caf50;
                    color: white;
                    border-radius: 6px;
                    display: flex;
                    justify-content: flex-start;
                    padding-left: 10px; /* Optional */
                }
                """,
        ):
            for lesson in lessons:
                if st.button(lesson["title"], use_container_width=True):
                    st.session_state.lesson_name = lesson["title"]
                    st.session_state.lesson_content = lesson["content"]
                    st.switch_page("pages.lesson_viewer.py")
