import streamlit as st
import utils 
import time
st.title(st.session_state.lesson_name)
st.write(st.session_state.lesson_content)
col1, col2, col3 = st.columns([1.6,1.5,6.9])
with col1:
    if st.button('Go back to the dashboard', use_container_width=True):
        utils.reset_and_navigate("pages/student_dashboard.py")
with col2:
    if st.button('Complete this lesson', use_container_width=True):
        utils.complete_lesson(st.session_state.lesson_id)
        st.balloons()
        time.sleep(3)
        utils.reset_and_navigate("pages/student_dashboard.py")