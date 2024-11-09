import streamlit as st
import streamlit.components.v1 as components
import utils
from streamlit_extras.stylable_container import stylable_container 

utils.restrict_access("student")

# Sample data
roadmap = ["Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4"]
completed_lessons = 2
total_lessons = len(roadmap)
xp = utils.get_user_xp()

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
    margin-bottom: 15px;
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
col1, col2, col3, col4, col5 = st.columns([5, 1, 2, 0.5, 1.5])
with col1:
    st.markdown('<h2 class="header-text">Hello, student!</h2>', unsafe_allow_html=True)
with col2:
    with stylable_container(
        key="level",
        css_styles=""" 
        .st-ah {
            margin: 0px;
            padding: 0px;
        }
        .levelLabel {
            font-size: 15px;
            margin-top: 60px;
            margin-bottom: 20px;
            padding: 0px;
            margin-left: 80px;
        }
        """,
    ):
        st.write("")
        st.write(f'<span class="levelLabel">Level 1</span>', unsafe_allow_html=True)
        # Display level
with col3:
    with stylable_container(
        key="progress",
        css_styles="""
        .nextLevelLabel {
            font-size: 15px;
            margin: 0px;
            padding: 0px;
        }
        """,
    ):
        progress_percentage = int(xp) / 1000
        st.progress(progress_percentage, f"{xp} XP / 1000 XP ({progress_percentage*100:.0f}%)")
                # Display XP
with col4:
    with stylable_container( key="logout",
            css_styles=""" 
            button {
                margin-top: 20px;
                color: white;
            }
            button:hover {
                border: 1px transparent black;
            }
                """,):
        if st.button("📊", help="Leaderboard"):
            utils.reset_and_navigate("pages/leaderboard.py")
with col5:
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
    completed_lessons = utils.get_completed_lessons()
    number_of_completed_lessons = len(completed_lessons)
    lessons = utils.get_lessons_student()
    number_of_lessons = len(lessons)
    xp = utils.get_user_xp()
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
        col1, col2, col3 = st.columns([0.5, 8, 1.5])
        with col1:
            with stylable_container(
                key="roadmap",
                css_styles="""
                .lesson {
                    font-size: 18px;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    },
                .stImage {
                    width: 8x;
                    height: 8px;
                    margin-right: 10000px;
                    }"""):
                st.markdown("""
                                <style>
                                .stImage {
                                    width: 40px;
                                    height: 40px;
                                    padding: 0px;
                                    margin-bottom: 5px;
                                }
                                </style>""", unsafe_allow_html=True)
                next_lesson = None
                for lesson in lessons:
                    if lesson['completed']:
                        st.write('<img src="https://img.icons8.com/ios-filled/50/4CAF50/checkmark.png" class="stImage"></div>', unsafe_allow_html=True)
                    else:
                        if not next_lesson:
                            st.write('<img src="data:image/png;base64,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" class="stImage"></div>', unsafe_allow_html=True)
                            next_lesson = lesson
                        else:
                            st.write('<img src="https://img.icons8.com/ios-filled/50/808080/lock.png" class="stImage">', unsafe_allow_html=True)
        with col2:
            with stylable_container(
                key="green_button",
                css_styles="""
                    button {
                        color: white;
                        border-radius: 6px;
                        line-height: 35px;
                        display: flex;
                        justify-content: flex-start;
                        padding-left: 10px; /* Optional: Adds padding on the left side */
                        background: #333;
                        border-color: white;
                        padding: 7px;
                    }
                    button:hover {
                        transform: scale(1.05);
                        transition: transform 0.2s;
                        border-color: white;
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
                    if lesson["completed"]:
                        st.markdown(f"""<div class="lesson completed">{lesson["title"]}</div>""", unsafe_allow_html=True)
                    elif lesson==next_lesson:
                        if st.button(lesson["title"], use_container_width=True):
                            st.session_state.lesson_name = lesson["title"]
                            st.session_state.lesson_content = lesson["content"]
                            st.session_state.lesson_id = lesson["_id"]
                            st.switch_page("pages/lesson_viewer.py")
                    else:
                        st.markdown(f"""<div class="lesson locked">{lesson["title"]}</div>""", unsafe_allow_html=True)
