import streamlit as st
import streamlit.components.v1 as components
import utils

#utils.restrict_access("student")

# Sample data
roadmap = ["Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4"]
completed_lessons = 2
total_lessons = len(roadmap)
xp = 150

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
with col2:
    if st.button("Logout"):
        utils.reset_and_navigate("pages/login.py")

st.markdown('<h2 class="header-text">Your progress</h2>', unsafe_allow_html=True)

# Display progress bar
progress_percentage = (completed_lessons / total_lessons)
st.progress(progress_percentage)

for i, lesson in enumerate(roadmap):
    icon_url = get_lesson_icon(i)
    icon_html = f"<img src='{icon_url}' alt='icon'>" if icon_url else ""
    lesson_class = "completed" if i < completed_lessons else "locked" if i > completed_lessons else ""
    st.markdown(f"<div class='lesson {lesson_class}'>{lesson} <span>{icon_html}</span></div>", unsafe_allow_html=True)

# Display XP
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
    <div style="margin-left: 20px;">
        <h3 style="margin: 0; font-size: 24px; color: #4CAF50;">XP: {xp}</h3>
    </div>
</div>
""", unsafe_allow_html=True)