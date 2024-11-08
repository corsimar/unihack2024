import streamlit as st
import streamlit.components.v1 as components

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
st.header("Your progress")
st.markdown("""
     <style>
    .lesson {
        font-size: 18px;
        margin-bottom: 10px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .lesson.completed {
        color: #4CAF50;
        border-color: #4CAF50;
    }
    .lesson.locked {
        color: #808080;
        border-color: #808080;
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
    </style>
    """, unsafe_allow_html=True)

# Display progress bar
progress_percentage = (completed_lessons / total_lessons)
st.progress(progress_percentage, f"XP: {xp}")

for i, lesson in enumerate(roadmap):
    icon_url = get_lesson_icon(i)
    icon_html = f"<img src='{icon_url}' alt='icon'>" if icon_url else ""
    lesson_class = "completed" if i < completed_lessons else "locked" if i > completed_lessons else ""
    st.markdown(f"<div class='lesson {lesson_class}'>{lesson} <span>{icon_html}</span></div>", unsafe_allow_html=True)
