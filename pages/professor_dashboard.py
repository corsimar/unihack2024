import streamlit as st
import utils
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="Dashboard", page_icon="📄")

# Create a button at the top right
col1, col2 = st.columns([8, 2])
# Create a top bar with the name RevoLearn on the left and profile on the right
with col2:
    if st.button("Create Lesson"):
        utils.reset_and_navigate("pages/lesson_editor.py")

lessons = [
    {"title": "Lesson 1", "thumbnail": "https://via.placeholder.com/350x150"},
    {"title": "Lesson 2", "thumbnail": "https://via.placeholder.com/350x150"},
    {"title": "Lesson 3", "thumbnail": "https://via.placeholder.com/350x150"},
    {"title": "Lesson 4", "thumbnail": "https://via.placeholder.com/350x150"},
    {"title": "Lesson 5", "thumbnail": "https://via.placeholder.com/350x150"},
    {"title": "Lesson 6", "thumbnail": "https://via.placeholder.com/350x150"},
]

for i in range(0, len(lessons), 3):
    cols = st.columns(3)
    for col, lesson in zip(cols, lessons[i:i+3]):
        with col:
            st.image(lesson["thumbnail"], use_container_width=True)
            if st.button(lesson['title'], key=f"view_{i}_{lesson['title']}"):
                utils.reset_and_navigate(f"pages/lesson_viewer.py?lesson={lesson['title']}")